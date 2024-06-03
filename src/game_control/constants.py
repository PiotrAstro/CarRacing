import os.path
import time
from pathlib import Path
from typing import Literal

import numpy as np

# randomize numpy seed
np.random.seed(int(time.time() * 1000) % 2**32)

AI_MODES = Literal["easy", "medium", "hard"]
NEURAL_NETWORKS_DIR = Path("networks")
IMAGES_DIR = Path("images")

PLAYER_CAR_CHANGEABLE_INIT = {
    "max_speed": 10.0,
    "min_speed": -1.0,
    "acceleration": 0.4,
    "turn_speed": 2.0,
    "inactive_steps": 60,
    "width_height": (20, 40),
}

MAX_AI_CARS = 4


# initial values, from list element will be chosen randomly
AI_CAR_CHANGEABLE_INIT = {
    "max_speed": [10, 20],
    "min_speed": -1.0,
    "acceleration": [0.1, 0.2],
    "turn_speed": 2.0,
    "inactive_steps": 120,
    "width_height": [(10, 20), (20, 40)],
    "mode": ["easy", "medium"],
}

# min, max step, min and max are included
CAR_CHANGEABLE_VALUES = {
    "max_speed": [5.0, 10.0, 20.0],
    "acceleration": [0.1, 0.2, 0.4],
    "width_height": [(10, 20), (20, 40), (35, 60)],
    "turn_speed": [1.0, 2.0, 4.0],  # [1.0, 2.0, 4.0],
    "inactive_steps": [i for i in range(0, 660, 60)],
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
    IMAGES_DIR / "spaceship0.png",
    IMAGES_DIR / "spaceship1.png",
    IMAGES_DIR / "spaceship2.png",
    IMAGES_DIR / "spaceship3.png",
    IMAGES_DIR / "spaceship4.png",
    IMAGES_DIR / "spaceship5.png",
]

LAPS_RANGE = (1, 8)
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
        "name": "Pillars of Creation",
        "x": 2707,
        "y": 2007,
        "start_angle": 95,
        "end_line": ((2663, 1975), (2748, 1972)),
        "false_end_line": ((2633, 1940), (2746, 1928)),
        "start_before_end_line": True,
        "bounding_map": IMAGES_DIR / "map_eagle.png",
        "image": IMAGES_DIR / "map_eagle.jpg",
    },
    {
        "name": "Spiral Death",
        "x": 6496,
        "y": 1806,
        "start_angle": 115,
        "end_line": ((2555, 3622), (2552, 3708)),
        "false_end_line": ((2525, 3622), (2522, 3708)),
        "start_before_end_line": False,
        "bounding_map": IMAGES_DIR / "map_quintet.png",
        "image": IMAGES_DIR / "map_quintet.jpg",
    },
]