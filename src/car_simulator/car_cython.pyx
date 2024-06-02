import dataclasses
import math
from libc.math cimport cos, sin, pi
import cython
import numpy as np
# from src.car_simulator.car_python import CarDrawInfo

@dataclasses.dataclass
class CarDrawInfo:
    x: int
    y: int
    angle_radians: float
    width: float
    height: float
    inactive_ratio: float


cdef class CarCython:
    cdef unsigned char [:, ::1] map_view
    cdef float x, y, angle, speed, max_speed, min_speed, acceleration, turn_speed
    cdef float width, height
    cdef float distance_center_corner
    cdef float angle_to_corner
    cdef float rays_distances_scale_factor
    cdef float ray_input_clip
    cdef float[::1] rays_degrees
    cdef int inactive_steps
    cdef int current_inactive_steps

    def __init__(self,
                 x: float,
                 y: float,
                 start_angle: float,
                 max_speed: float,
                 min_speed: float,
                 acceleration: float,
                 turn_speed: float,
                 inactive_steps: int,
                 map_view: np.ndarray,  # Assuming 2D array
                 width: float,
                 height: float,
                 rays_distances_scale_factor: float,
                 ray_input_clip: float,
                 rays_degrees: list[float] | tuple[float] | np.ndarray) -> None:
        self.x = x
        self.y = y
        self.angle = math.radians(start_angle)
        self.speed = 0.0
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.acceleration = acceleration
        self.turn_speed = math.radians(turn_speed)
        self.inactive_steps = inactive_steps if inactive_steps > 0 else 1
        self.rays_degrees = np.array(
            [math.radians(ray) for ray in rays_degrees], dtype=np.float32
        )
        self.map_view = map_view
        self.width = width
        self.height = height
        self.rays_distances_scale_factor = rays_distances_scale_factor
        self.ray_input_clip = ray_input_clip
        self.current_inactive_steps = 0

        self.distance_center_corner = math.sqrt((self.width / 2) ** 2 + (self.height / 2) ** 2)
        self.angle_to_corner = math.atan2(self.width / 2, self.height / 2)

        self.react(0.0, 0.0)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def nn_state(self) -> np.ndarray:
        cdef float[::1] rays_degrees_here = self.rays_degrees
        cdef float[::1] state_here = np.empty(self.rays_degrees.shape[0] + 1, dtype=np.float32)

        for i in range(self.rays_degrees.shape[0]):
            state_here[i] = self._get_ray_distance(rays_degrees_here[i]) / self.rays_distances_scale_factor
            if state_here[i] > self.ray_input_clip:
                state_here[i] = self.ray_input_clip

        state_here[state_here.shape[0] - 1] = self.speed / self.max_speed

        return np.array(state_here, dtype=np.float32, copy=False)

    def get_draw_info(self) -> CarDrawInfo:
        return CarDrawInfo(round_to_int(self.x), round_to_int(self.y), self.angle, self.width, self.height, self.get_inactive_ratio())

    def get_position(self) -> tuple[float, float]:
        return self.x, self.y

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef double _get_ray_distance(self, double ray_angle):
        cdef unsigned char [:, ::1] map_view_here = self.map_view
        cdef double x = self.x
        cdef double y = self.y
        cdef double distance = 0
        cdef int check_x, check_y
        cdef double angle = self.angle + ray_angle
        cdef double sin_angle = sin(angle)
        cdef double cos_angle = cos(angle)

        check_x = round_to_int(x)
        check_y = round_to_int(y)

        while check_x >= 0 and check_x < map_view_here.shape[1] and check_y >= 0 and check_y < map_view_here.shape[0] and map_view_here[check_y, check_x] == 0:
            x += cos_angle
            y -= sin_angle
            distance += 1
            check_x = round_to_int(x)
            check_y = round_to_int(y)

        return distance


    def react(self, float engine, float steering) -> None:
        engine = max(-1.0, min(1.0, engine))
        steering = max(-1.0, min(1.0, steering))

        # Wheel traction
        cdef float traction = self.speed / self.max_speed
        engine -= traction

        self.speed += engine * self.acceleration
        self.speed = max(self.min_speed, min(self.max_speed, self.speed))
        self.angle += steering * self.turn_speed
        if self.angle > 2 * pi:
            self.angle -= 2 * pi
        elif self.angle < 0:
            self.angle += 2 * pi

    def get_speed(self) -> float:
        return self.speed

    def stop(self) -> None:
        self.speed = 0.0

    def step(self) -> None:
        if self.current_inactive_steps > 0:
            self.current_inactive_steps -= 1
        else:
            self.x += self.speed * cos(self.angle)
            self.y -= self.speed * sin(self.angle)
            if self._does_collide():
                self._fix_collision()
                self.current_inactive_steps = self.inactive_steps
                self.speed = 0.0
                self.react(0.0, 0.0)

    def get_inactive_ratio(self) -> float:
        return self.current_inactive_steps / (<float> self.inactive_steps)


    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef void _fix_collision(self):
        # get angle of the wall by checking many angles around current position of the car
        cdef float[::1] angles = np.linspace(0, 2 * pi, 90, endpoint=False, dtype=np.float32)
        cdef unsigned char [::1] collisions = np.empty(angles.shape[0], dtype=np.uint8)
        cdef float checked_distance = self.distance_center_corner * 1.5
        cdef int i
        for i in range(angles.shape[0]):
            collisions[i] = self._does_collide_one(checked_distance, angles[i])

        # get index of start and end of the longest sequence of collisions
        cdef int start = 0
        cdef int end = 0
        cdef int current_start = 0
        cdef int current_end = 0
        cdef int max_length = 0
        cdef int current_length = 0
        cdef int current_index
        for current_index in range(collisions.shape[0] * 2):
            current_index = current_index % collisions.shape[0]
            if collisions[current_index] == 1:
                if current_length == 0:
                    current_start = current_index
                current_length += 1
                current_end = current_index
            else:
                if current_length > max_length:
                    max_length = current_length
                    start = current_start
                    end = current_end
                current_length = 0

        # get angle of the wall
        cdef float angle_between = angles[end] - angles[start]
        if angle_between < 0:
            angle_between += 2 * pi
        if angle_between > pi:
            angle_between = 2 * pi - angle_between

        cdef float perpendicular_wall_angle = (angles[start] + angle_between / 2)
        cdef float wall_angle = perpendicular_wall_angle + pi / 2
        if wall_angle > 2 * pi:
            wall_angle -= 2 * pi

        # check if I should set the angle to the wall angle or to the opposite angle
        cdef float angle_diff = abs(self.angle - wall_angle)
        if angle_diff > pi / 2 and angle_diff < 3 / 2 * pi:
            wall_angle -= pi
        self.angle = wall_angle

        # calculate distance from current car position to the wall
        cdef float move_distance = 0.2 * self.width # - self.distance_center_corner * cos(angle_between / 2)
        cdef bint end_trigger = False
        perpendicular_wall_angle -= pi

        for i in range(10):
            if not self._does_collide():
                end_trigger = True
            self.x += move_distance * cos(perpendicular_wall_angle)
            self.y -= move_distance * sin(perpendicular_wall_angle)

            if end_trigger:
                break

        # finished :)



    cdef bint _does_collide(self):
        return (self._does_collide_one(self.distance_center_corner, self.angle - self.angle_to_corner) or
                self._does_collide_one(self.distance_center_corner, self.angle + self.angle_to_corner) or
                self._does_collide_one(self.distance_center_corner, pi + self.angle - self.angle_to_corner) or
                self._does_collide_one(self.distance_center_corner, pi + self.angle + self.angle_to_corner) or
                self._does_collide_one(self.width / 2, self.angle + pi/2) or
                self._does_collide_one(self.width / 2, self.angle - pi/2) or
                self._does_collide_one(self.height / 2, self.angle) or
                self._does_collide_one(self.height / 2, self.angle + pi))
    @cython.initializedcheck(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef bint _does_collide_one(self, double distance, double angle):
        cdef int check_x, check_y
        check_x = round_to_int(self.x + distance * cos(angle))
        check_y = round_to_int(self.y - distance * sin(angle))

        if check_x < 0 or check_x >= self.map_view.shape[1]:
            return True
        if check_y < 0 or check_y >= self.map_view.shape[0]:
            return True

        return self.map_view[check_y, check_x] == 1

cdef inline int round_to_int(double value):
    """
    Round the given value to the nearest integer.
    """
    return <int>(value + 0.5)

def check_crossed_line(line: tuple[tuple[int, int], tuple[int, int]], previous_position: tuple[float, float],
                       current_position: tuple[float, float]) -> bool:
    cdef float x1, y1, x2, y2
    cdef float x3, y3, x4, y4
    cdef float denom, ua, ub

    # Unpack line endpoints
    (x1, y1), (x2, y2) = line

    # Unpack positions
    x3, y3 = previous_position
    x4, y4 = current_position

    # Check if the previous and current positions are the same
    if x3 == x4 and y3 == y4:
        return False

    # Calculate the denominator
    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)

    # Check if lines are parallel
    if denom == 0:
        return False

    # Calculate the intersection point
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

    # Check if intersection point lies on both line segments
    return 0 <= ua <= 1 and 0 <= ub <= 1
