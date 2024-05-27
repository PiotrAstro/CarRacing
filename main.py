import sys
from PySide6.QtWidgets import QApplication

from src.GUI.main_menu import MainMenu
from src.game_control.game_controller import GameController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game_controller = GameController()
    window = MainMenu(game_controller)
    window.show()
    sys.exit(app.exec())