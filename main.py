import sys
from PySide6.QtWidgets import QApplication

from src.GUI.main_window import MainWindow
from src.game_control.game_controller import GameController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game_controller = GameController()
    window = MainWindow(game_controller)
    window.show()
    sys.exit(app.exec())
