import os.path
from pathlib import Path

IMAGES_DIR = Path(os.path.join(__file__, "..", "..", "images"))

PLAYER_CAR_CHANGEABLE_INIT = {
    "max_speed": 5,
    "min_speed": -1,
    "acceleration": 0.1,
    "turn_speed": 0.1,
    "inactive_steps": 10,
    "width": 10,
    "height": 20,
}

MAX_AI_CARS = 6

AI_CAR_CHANGEABLE_INIT = {
    "max_speed": 5,
    "min_speed": -1,
    "acceleration": 0.1,
    "turn_speed": 0.1,
    "inactive_steps": 10,
    "width": 10,
    "height": 20,
}

CAR_CHANGEABLE_RANGE = {
    "max_speed": (0, 10),
    "min_speed": (-2, 0),
    "acceleration": (0, 0.2),
    "turn_speed": (0, 0.2),
    "inactive_steps": (0, 20),
    "width": (5, 15),
    "height": (10, 30),
}

AI_STRUCTURE = {
    "rays_distances_scale_factor": 100.0,
    "ray_input_clip": 5.0,
    "rays_degrees": (-90, -67.5, -45, -22.5, 0, 22.5, 45, 67.5, 90),
    "neural_network": {
        "input_normal_size": 10,
        "out_actions_number": 4,
        "normal_hidden_layers": 2,
        "normal_hidden_neurons": 64,
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

MAPS = [
    {
        "name": "Easy Peasy",
        "x": 0,
        "y": 0,
        "start_angle": 0,
        "end_line": ((0, 0), (0, 100)),
        "false_end_line": ((0, 0), (0, 100)),
        "start_before_end_line": True,
        "bounding_map": IMAGES_DIR / "map1_walls.png",
        "image": IMAGES_DIR / "map1.png",
    },
]