from PySide6.QtWidgets import QMainWindow, QStackedWidget, QPushButton, QVBoxLayout, QWidget, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

from src.GUI.setting_pages import MapSettingsPage, PlayerSettingsPage, AISettingsPage
from src.GUI.styles import BUTTON_STYLE, MAIN_MENU_BACKGROUND


class MainMenu(QMainWindow):
    def __init__(self, game_controller):
        super(MainMenu, self).__init__()
        self.setWindowTitle("AI Car Racing")
        self.setGeometry(100, 100, 800, 600)
        self.game_controller = game_controller

        # Create the stacked widget
        self.stacked_widget = QStackedWidget()

        # Create the main menu page
        self.main_menu = QWidget()
        self.main_menu_layout = QVBoxLayout()

        # Add title label
        self.title_label = QLabel("AI Car Racing")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('Arial', 36))
        self.title_label.setStyleSheet("color: white;")
        self.main_menu_layout.addWidget(self.title_label, stretch=1)

        # Spacer item to push buttons towards the center
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_menu_layout.addItem(spacer_top)

        self.map_button = QPushButton("Choose Map")
        self.map_button.setStyleSheet(BUTTON_STYLE)
        self.map_button.clicked.connect(self.show_map_settings)
        self.main_menu_layout.addWidget(self.map_button, stretch=1)

        self.player_settings_button = QPushButton("Player Settings")
        self.player_settings_button.setStyleSheet(BUTTON_STYLE)
        self.player_settings_button.clicked.connect(self.show_player_settings)
        self.main_menu_layout.addWidget(self.player_settings_button, stretch=1)

        self.ai_settings_button = QPushButton("AI Settings")
        self.ai_settings_button.setStyleSheet(BUTTON_STYLE)
        self.ai_settings_button.clicked.connect(self.show_ai_settings)
        self.main_menu_layout.addWidget(self.ai_settings_button, stretch=1)

        self.play_button = QPushButton("Play Game")
        self.play_button.setStyleSheet(BUTTON_STYLE)
        self.play_button.clicked.connect(self.play_game)
        self.main_menu_layout.addWidget(self.play_button, stretch=1)

        # Spacer item to push buttons towards the center
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_menu_layout.addItem(spacer_bottom)

        # Create a container widget to hold the layout
        self.container = QWidget()
        self.container.setLayout(self.main_menu_layout)
        self.container.setStyleSheet("background: transparent;")

        # Create a central widget with background image
        central_widget = QWidget()
        central_widget.setStyleSheet(f"""
                background-image: url({MAIN_MENU_BACKGROUND});
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            """)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.container)

        self.main_menu.setLayout(central_layout)
        self.stacked_widget.addWidget(self.main_menu)

        # Create and add settings pages
        self.map_settings_page = MapSettingsPage(self, self.game_controller)
        self.player_settings_page = PlayerSettingsPage(self, self.game_controller)
        self.ai_settings_page = AISettingsPage(self, self.game_controller)

        self.stacked_widget.addWidget(self.map_settings_page)
        self.stacked_widget.addWidget(self.player_settings_page)
        self.stacked_widget.addWidget(self.ai_settings_page)

        # Set the stacked widget as the central widget
        self.setCentralWidget(self.stacked_widget)

    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def show_map_settings(self):
        self.stacked_widget.setCurrentWidget(self.map_settings_page)

    def show_player_settings(self):
        self.stacked_widget.setCurrentWidget(self.player_settings_page)

    def show_ai_settings(self):
        self.stacked_widget.setCurrentWidget(self.ai_settings_page)

    def play_game(self):
        map_setting = self.game_controller.get_map_setting()
        player_settings = self.game_controller.get_player_settings()
        ai_setting = self.game_controller.get_ai_setting()

        print(f"Starting game with settings: Map={map_setting}, Player={player_settings}, AI={ai_setting}")