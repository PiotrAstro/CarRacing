import dataclasses
import time
from abc import ABC, abstractmethod
from typing import Any, Literal

import keyboard
import numpy as np

from src.car_simulator.car_cython import CarCython, check_crossed_line
from src.car_training.Neural_Network.Raw_Numpy.Raw_Numpy_Models.Normal.Normal_model import Normal_model

Line = tuple[tuple[int, int], tuple[int, int]]
Steering_Method = Literal["WSAD", "Arrows"]

# randomize numpy seed
np.random.seed(time.time() * 1000 % 2**32)

@dataclasses.dataclass
class CarDrawInfo:
    x: int
    y: int
    angle_radians: float
    width: float
    height: float
    inactive_ratio: float


class CarWrapper(ABC):
    car: CarCython
    laps: list[int]
    previous_position: tuple[float, float]
    end_line: Line
    false_end_line: Line
    end_line_balance: int
    false_end_line_balance: int
    time_counter: int
    max_laps: int

    def __init__(self, car_init_data: dict[str, Any], end_line: Line, false_end_line: Line, start_before_end_line: bool, max_laps: int):
        self.car = CarCython(**car_init_data)
        self.laps = []
        self.end_line = end_line
        self.false_end_line = false_end_line
        self.end_line_balance = 0
        self.false_end_line_balance = 0
        self.start_before_end_line = start_before_end_line
        self.previous_position = self.car.get_position()
        self.time_counter = 0
        self.max_laps = max_laps

    def get_car_draw_info(self) -> CarDrawInfo:
        return self.car.get_draw_info()

    @abstractmethod
    def react(self) -> tuple[float, float]:
        """
        This function should return engine and steering
        :return:
        """
        pass

    def step(self):
        self.time_counter += 1

        if self.car.get_inactive_ratio() == 0.0:
            engine, steering = self.react()
            if len(self.laps) >= self.max_laps:
                engine = -1.0
            self.car.react(engine, steering)
            self.car.step()
            self._laps_calculations()
        else:
            self.car.step()

    def _laps_calculations(self) -> None:
        new_position = self.car.get_position()

        if check_crossed_line(self.end_line, self.previous_position, new_position):
            if self.start_before_end_line:
                self.start_before_end_line = False
                self.false_end_line_balance = -1
            if self.end_line_balance == 0:
                self.laps.append(self.time_counter)
                self.false_end_line_balance = -1
            elif self.end_line_balance < 0:
                self.end_line_balance += 1
        if check_crossed_line(self.false_end_line, self.previous_position, new_position):
            if self.false_end_line_balance < 0:
                self.false_end_line_balance += 1
            elif self.false_end_line_balance == 0:
                self.end_line_balance -= 1

        self.previous_position = new_position


class CarPlayerWrapper(CarWrapper):
    steering_method: Steering_Method

    def __init__(self, steering_method: Steering_Method, car_init_data: dict[str, Any], end_line: Line, false_end_line: Line, start_before_end_line: bool, max_laps: int):
        super().__init__(car_init_data, end_line, false_end_line, start_before_end_line, max_laps)
        self.steering_method = steering_method

    def react(self) -> tuple[float, float]:
        engine = 0.0
        steering = 0.0
        if self.steering_method == "WSAD":
            if keyboard.is_pressed("w"):
                engine = 1.0
            elif keyboard.is_pressed("s"):
                engine = -1.0

            if keyboard.is_pressed("a"):
                steering = -1.0
            elif keyboard.is_pressed("d"):
                steering = 1.0
        elif self.steering_method == "Arrows":
            if keyboard.is_pressed("up"):
                engine = 1.0
            elif keyboard.is_pressed("down"):
                engine = -1.0

            if keyboard.is_pressed("left"):
                steering = -1.0
            elif keyboard.is_pressed("right"):
                steering = 1.0
        return engine, steering


class CarAIWrapper(CarWrapper):
    model: Normal_model
    random_action_prob: float

    def __init__(self,
                 neural_network_structure: dict[str, Any],
                 neural_network_params: dict[str, Any],
                 random_action_prob: float,
                 car_init_data: dict[str, Any],
                 end_line: Line,
                 false_end_line: Line,
                 start_before_end_line: bool,
                 max_laps: int):
        super().__init__(car_init_data, end_line, false_end_line, start_before_end_line, max_laps)
        self.model = Normal_model(**neural_network_structure)
        self.model.set_parameters(neural_network_params)
        self.random_action_prob = random_action_prob

    def react(self) -> tuple[float, float]:
        nn_input = self.car.nn_state()

        if np.random.rand() < self.random_action_prob:
            nn_output = np.random.uniform(-1.0, 1.0, 4)
        else:
            nn_output = self.model.p_forward_pass(nn_input)

        max_index = np.argmax(nn_output[:3])
        steering = 0.0
        match max_index:
            case 0:
                steering = 1.0
            case 1:
                steering = -1.0

        engine = nn_output[3]
        return engine, steering


class GameSimulation:
    cars_ai: list[CarWrapper]
    cars_players: list[CarWrapper]
    max_timesteps: int
    current_timestep: int
    def __init__(self,
                 car_ai_inits: list[tuple[dict[str, Any], dict[str, Any], float]],  # car_init, neural_network_params, percent_of_random_decisions
                 car_players_init: list[tuple[Steering_Method, dict[str, Any]]],
                 map: np.ndarray,
                 neural_network_structure: dict[str, Any],
                 max_timesteps: int,
                 end_line: Line,
                 false_end_line: Line,
                 start_before_end_line: bool = False,
                 lap_number: int = 3,
                 ):
        self.max_timesteps = max_timesteps
        for car_ai_init, _, _ in car_ai_inits:
            car_ai_init["map"] = map

        self.cars_ai = [
            CarAIWrapper(
                neural_network_structure,
                ai_params,
                random_action_prob,
                car_init,
                end_line,
                false_end_line,
                start_before_end_line,
                lap_number
            ) for car_init, ai_params, random_action_prob in car_ai_inits]

        for _, car_init in car_players_init:
            car_init["map"] = map

        self.cars_players = [
            CarPlayerWrapper(
                steering_method,
                car_init,
                end_line,
                false_end_line,
                start_before_end_line,
                lap_number
            ) for steering_method, car_init in car_players_init]

    def step(self):
        for car in self.cars_ai:
            car.step()
        for car in self.cars_players:
            car.step()
        self.current_timestep += 1

    def is_finished(self) -> bool:
        return all([len(car.laps) >= car.max_laps for car in self.cars_players]) or self.current_timestep >= self.max_timesteps
