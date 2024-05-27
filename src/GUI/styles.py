import os
from pathlib import Path

IMAGES_GUI_DIR = Path(os.path.join(__file__, "..", "..", "images"))

MAIN_MENU_BACKGROUND = r"C:\Piotr\2024_studia\semestr_4\Skryptowe\Laby\CarRacing\images\main_background.jpg"#IMAGES_GUI_DIR / "main_background.jpg"

BUTTON_STYLE = """
    QPushButton {
        font-size: 24px;
        color: white;
        background-color: #333;
        border: 1px solid #555;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #444;
    }
    QPushButton:pressed {
        background-color: #555;
    }
"""