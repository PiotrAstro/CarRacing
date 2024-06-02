from PySide6.QtWidgets import QMainWindow, QStackedWidget

from src.GUI.game import GamePage
from src.GUI.main_menu import MainMenuWidget
from src.GUI.map_settings import MapSettingsPage
from src.GUI.player_settings import PlayerSettingsPage


class MainWindow(QMainWindow):
    def __init__(self, game_controller):
        super(MainWindow, self).__init__()
        self.setWindowTitle("AI Car Racing")
        self.setGeometry(100, 100, 800, 600)
        self.game_controller = game_controller

        # Create the stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Main menu page
        self.main_menu_page = MainMenuWidget(self.game_controller, self, self)
        self.stacked_widget.addWidget(self.main_menu_page)

        # Create and add settings pages
        self.map_settings_page = MapSettingsPage(self.game_controller, self, self)
        self.player_settings_page = PlayerSettingsPage(self.game_controller, self, self)
        self.game_page = GamePage(self.game_controller, self, self)

        self.stacked_widget.addWidget(self.map_settings_page)
        self.stacked_widget.addWidget(self.player_settings_page)
        self.stacked_widget.addWidget(self.game_page)

    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu_page)

    def show_map_settings(self):
        self.stacked_widget.setCurrentWidget(self.map_settings_page)

    def show_player_settings(self):
        self.stacked_widget.setCurrentWidget(self.player_settings_page)

    def play_game(self):
        self.game_page.start_game()
        self.stacked_widget.setCurrentWidget(self.game_page)

