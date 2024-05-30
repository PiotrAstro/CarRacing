import os.path
import time
from pathlib import Path

import numpy as np

# randomize numpy seed
np.random.seed(int(time.time() * 1000) % 2**32)

NEURAL_NETWORKS_DIR = Path("networks")
IMAGES_DIR = Path("images")

PLAYER_CAR_CHANGEABLE_INIT = {
    "max_speed": 10,
    "min_speed": -1,
    "acceleration": 0.1,
    "turn_speed": 2,
    "inactive_steps": 60,
    "width": 10,
    "height": 20,
}

MAX_AI_CARS = 3

AI_CAR_CHANGEABLE_INIT = {
    "max_speed": 6,
    "min_speed": -1.2,
    "acceleration": 0.04,
    "turn_speed": 1.2,
    "inactive_steps": 120,
    "width": 35,
    "height": 70,
}

CAR_CHANGEABLE_RANGE = {
    "max_speed": (0, 10),
    "min_speed": (-2, 0),
    "acceleration": (0, 0.2),
    "turn_speed": (0, 0.2),
    "inactive_steps": (0, 600),
    "width": (5, 35),
    "height": (10, 70),
}

AI_STRUCTURE = {
    "rays_distances_scale_factor": 100.0,
    "ray_input_clip": 5.0,
    "rays_degrees": (-90, -45, 0, 45, 90),  # (-90, -67.5, -45, -22.5, 0, 22.5, 45, 67.5, 90),
    "neural_network": {
        "input_normal_size": 6,
        "out_actions_number": 4,
        "normal_hidden_layers": 2,
        "normal_hidden_neurons": 128,
        "normal_activation_function": "relu",  # "relu"
        "last_activation_function": [("softmax", 3), ("tanh", 1)],
    },
}

CARS = [
    IMAGES_DIR / "car1.png",
    IMAGES_DIR / "car2.png",
    IMAGES_DIR / "car3.png",
    IMAGES_DIR / "car4.png",
    IMAGES_DIR / "car5.png",
    IMAGES_DIR / "car6.png",
]

LAPS_RANGE = (1, 10)
SECONDS_RANGE = (30, 1200)
FPS = 60
DEFAULT_SECONDS = 120

MAPS = [
    {
        "name": "Easy Peasy",
        "x": 2336,
        "y": 3025,
        "start_angle": 60,
        "end_line": ((2334, 2985), (2373, 3010)),
        "false_end_line": ((2353, 2956), (2390, 2982)),
        "start_before_end_line": True,
        "bounding_map": IMAGES_DIR / "map_orion_walls.png",
        "image": IMAGES_DIR / "map_orion.jpg",
    },
    {
        "name": "Harder Squazzle",
        "x": 0,
        "y": 0,
        "start_angle": 0,
        "end_line": ((0, 0), (0, 100)),
        "false_end_line": ((0, 0), (0, 100)),
        "start_before_end_line": False,
        "bounding_map": IMAGES_DIR / "map1_walls.png",
        "image": IMAGES_DIR / "map_orion.jpg",
    },
    {
        "name": "Harder Squazzle",
        "x": 0,
        "y": 0,
        "start_angle": 0,
        "end_line": ((0, 0), (0, 100)),
        "false_end_line": ((0, 0), (0, 100)),
        "start_before_end_line": True,
        "bounding_map": IMAGES_DIR / "map1_walls.png",
        "image": IMAGES_DIR / "map_orion.jpg",
    },
    {
        "name": "Harder Squazzle",
        "x": 0,
        "y": 0,
        "start_angle": 0,
        "end_line": ((0, 0), (0, 100)),
        "false_end_line": ((0, 0), (0, 100)),
        "start_before_end_line": True,
        "bounding_map": IMAGES_DIR / "map1_walls.png",
        "image": IMAGES_DIR / "map_orion.jpg",
    },
]