import dataclasses
import pickle
from abc import abstractmethod
from pathlib import Path
from typing import Literal

import numpy as np
from PIL import Image

from src.car_simulator.car_python import CarWrapper, Line, CarAIWrapper, CarPlayerWrapper, \
    GameSimulation
from src.game_control.constants import CAR_CHANGEABLE_RANGE, AI_STRUCTURE, PLAYER_CAR_CHANGEABLE_INIT, CARS, MAPS, \
    AI_CAR_CHANGEABLE_INIT, MAX_AI_CARS, FPS, DEFAULT_SECONDS, NEURAL_NETWORKS_DIR


class CarDataHolder:
    name: str
    image: Path
    max_speed: float
    min_speed: float
    acceleration: float
    turn_speed: float
    inactive_steps: int
    width: float
    height: float

    # def set_min_speed(self, min_speed: float):
    #     self.min_speed = min(max(min_speed, CAR_CHANGEABLE_RANGE["min_speed"][0]), CAR_CHANGEABLE_RANGE["min_speed"][1])
    #
    # def set_max_speed(self, max_speed: float):
    #     self.max_speed = min(max(max_speed, CAR_CHANGEABLE_RANGE["max_speed"][0]), CAR_CHANGEABLE_RANGE["max_speed"][1])
    #
    # def set_acceleration(self, acceleration: float):
    #     self.acceleration = min(max(acceleration, CAR_CHANGEABLE_RANGE["acceleration"][0]), CAR_CHANGEABLE_RANGE["acceleration"][1])
    #
    # def set_turn_speed(self, turn_speed: float):
    #     self.turn_speed = min(max(turn_speed, CAR_CHANGEABLE_RANGE["turn_speed"][0]), CAR_CHANGEABLE_RANGE["turn_speed"][1])
    #
    # def set_inactive_steps(self, inactive_steps: int):
    #     self.inactive_steps = min(max(inactive_steps, CAR_CHANGEABLE_RANGE["inactive_steps"][0]), CAR_CHANGEABLE_RANGE["inactive_steps"][1])
    #
    # def set_width(self, width: float):
    #     self.width = min(max(width, CAR_CHANGEABLE_RANGE["width"][0]), CAR_CHANGEABLE_RANGE["width"][1])
    #
    # def set_height(self, height: float):
    #     self.height = min(max(height, CAR_CHANGEABLE_RANGE["height"][0]), CAR_CHANGEABLE_RANGE["height"][1])

    @abstractmethod
    def create_car_wrapper(self, x: float, y: float, start_angle: float, map_view: np.ndarray, end_line: Line, false_end_line: Line, start_before_end_line: bool, max_laps: int) -> CarWrapper:
        pass

@dataclasses.dataclass
class CarPlayerDataHolder(CarDataHolder):

    def __init__(self, name: str, image: Path):
        self.name = name
        self.image = image
        self.max_speed = PLAYER_CAR_CHANGEABLE_INIT["max_speed"]
        self.min_speed = PLAYER_CAR_CHANGEABLE_INIT["min_speed"]
        self.acceleration = PLAYER_CAR_CHANGEABLE_INIT["acceleration"]
        self.turn_speed = PLAYER_CAR_CHANGEABLE_INIT["turn_speed"]
        self.inactive_steps = PLAYER_CAR_CHANGEABLE_INIT["inactive_steps"]
        self.width = PLAYER_CAR_CHANGEABLE_INIT["width"]
        self.height = PLAYER_CAR_CHANGEABLE_INIT["height"]

    def create_car_wrapper(self, x: float, y: float, start_angle: float, map_view: np.ndarray, end_line: Line, false_end_line: Line, start_before_end_line: bool, max_laps: int) -> CarPlayerWrapper:
        car_init_data = {
            "x": x,
            "y": y,
            "start_angle": start_angle,
            "max_speed": self.max_speed,
            "min_speed": self.min_speed,
            "acceleration": self.acceleration,
            "turn_speed": self.turn_speed,
            "inactive_steps": self.inactive_steps,
            "map_view": map_view,
            "width": self.width,
            "height": self.height,
            "rays_distances_scale_factor": 1.0,
            "ray_input_clip": 1.0,
            "rays_degrees": [],
        }

        return CarPlayerWrapper(
            car_init_data=car_init_data,
            end_line=end_line,
            false_end_line=false_end_line,
            start_before_end_line=start_before_end_line,
            max_laps=max_laps,
            name=self.name,
            image=self.image,
        )

    def set_name(self, name: str):
        if name != "":
            self.name = name[:20 if len(name) > 20 else len(name)]


@dataclasses.dataclass
class CarAIDataHolder(CarDataHolder):
    mode: Literal["easy", "medium", "hard"]
    active: bool

    def __init__(self, name: str, image: Path, mode: Literal["easy", "medium", "hard"] = "easy"):
        self.name = name
        self.image = image
        self.mode = mode
        self.active = True
        self.max_speed = AI_CAR_CHANGEABLE_INIT["max_speed"]
        self.min_speed = AI_CAR_CHANGEABLE_INIT["min_speed"]
        self.acceleration = AI_CAR_CHANGEABLE_INIT["acceleration"]
        self.turn_speed = AI_CAR_CHANGEABLE_INIT["turn_speed"]
        self.inactive_steps = AI_CAR_CHANGEABLE_INIT["inactive_steps"]
        self.width = AI_CAR_CHANGEABLE_INIT["width"]
        self.height = AI_CAR_CHANGEABLE_INIT["height"]

    def create_car_wrapper(self, x: float, y: float, start_angle: float, map_view: np.ndarray, end_line: Line, false_end_line: Line, start_before_end_line: bool, max_laps: int) -> CarAIWrapper:
        car_init_data = {
            "x": x,
            "y": y,
            "start_angle": start_angle,
            "max_speed": self.max_speed,
            "min_speed": self.min_speed,
            "acceleration": self.acceleration,
            "turn_speed": self.turn_speed,
            "inactive_steps": self.inactive_steps,
            "map_view": map_view,
            "width": self.width,
            "height": self.height,
            "rays_distances_scale_factor": AI_STRUCTURE["rays_distances_scale_factor"],
            "ray_input_clip": AI_STRUCTURE["ray_input_clip"],
            "rays_degrees": AI_STRUCTURE["rays_degrees"],
        }

        # TODO: load correct ai model and set random action prob
        with open(NEURAL_NETWORKS_DIR / "best_individual_1717031742_f1550.7.pkl", "rb") as f:
            nn_params = pickle.load(f)
        random_action_prob = 0.0


        return CarAIWrapper(
            neural_network_structure=AI_STRUCTURE["neural_network"],
            neural_network_params=nn_params,
            random_action_prob=random_action_prob,
            car_init_data=car_init_data,
            end_line=end_line,
            false_end_line=false_end_line,
            start_before_end_line=start_before_end_line,
            max_laps=max_laps,
            name=self.name,
            image=self.image,
        )

class GameController:
    ai_players: list[CarAIDataHolder]
    player: CarPlayerDataHolder
    selected_map: int
    map_laps: int
    map_max_timesteps: int

    def __init__(self):
        self.player = CarPlayerDataHolder("Player", CARS[0])
        self.ai_players = [
            CarAIDataHolder(f"AI {i}", CARS[i % len(CARS)]) for i in range(1, MAX_AI_CARS + 1)
        ]
        self.selected_map = 0
        self.map_laps = 3 if MAPS[self.selected_map]["start_before_end_line"] else 1
        self.map_max_timesteps = DEFAULT_SECONDS * FPS

    def set_max_seconds(self, max_timesteps: int):
        self.map_max_timesteps = max(max_timesteps * FPS, 1)

    def get_max_seconds(self):
        return self.map_max_timesteps / FPS

    def get_map_name(self) -> str:
        return MAPS[self.selected_map]["name"]

    def get_all_maps(self) -> list[tuple[str, Path]]:
        return [
            (map_tmp["name"], map_tmp["image"]) for map_tmp in MAPS
        ]

    def get_map_image(self) -> Path:
        return MAPS[self.selected_map]["image"]

    def create_game_simulation(self) -> GameSimulation:
        img = Image.open(MAPS[self.selected_map]["bounding_map"]).convert('L')  # 'L' stands for luminance
        map_view = np.array(np.array(img) / 255, dtype=np.bool_)
        map_data_tmp = MAPS[self.selected_map]
        x = map_data_tmp["x"]
        y = map_data_tmp["y"]
        start_angle = map_data_tmp["start_angle"]
        end_line = Line(map_data_tmp["end_line"])
        false_end_line = Line(map_data_tmp["false_end_line"])
        start_before_end_line = map_data_tmp["start_before_end_line"]

        cars_ai = [
            ai.create_car_wrapper(
                x=x,
                y=y,
                start_angle=start_angle,
                map_view=map_view,
                end_line=end_line,
                false_end_line=false_end_line,
                start_before_end_line=start_before_end_line,
                max_laps=self.map_laps
            ) for ai in self.ai_players if ai.active
        ]

        players = [
            self.player.create_car_wrapper(
                x=x,
                y=y,
                start_angle=start_angle,
                map_view=map_view,
                end_line=end_line,
                false_end_line=false_end_line,
                start_before_end_line=start_before_end_line,
                max_laps=self.map_laps
            )
        ]

        return GameSimulation(
            cars_ai=cars_ai,
            cars_players=players,
            max_timesteps=self.map_max_timesteps
        )

