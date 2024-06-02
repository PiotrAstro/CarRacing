from PySide6.QtGui import QFont, Qt, QPixmap, QPainter
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QComboBox, QPushButton, QSpacerItem, \
    QSizePolicy

from src.GUI.styles import BUTTON_STYLE, MAIN_MENU_BACKGROUND, WidgetBackgroundImage
from src.game_control.game_controller import GameController


class MainMenuWidget(WidgetBackgroundImage):
    def __init__(self, game_controller: GameController, parent, main_window):
        super(MainMenuWidget, self).__init__(MAIN_MENU_BACKGROUND, parent, alpha_overlay=0.0)
        self.game_controller = game_controller
        self.main_menu = main_window
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())

        # Title label
        title_label = QLabel("AI Car Racing")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 36))
        title_label.setStyleSheet("color: white;")
        self.layout().addWidget(title_label, stretch=1)

        # Spacer
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout().addItem(spacer_top)

        map_button = QPushButton("Choose Map")
        map_button.setStyleSheet(BUTTON_STYLE)
        map_button.clicked.connect(self.show_map_settings)
        self.layout().addWidget(map_button, stretch=1)

        player_settings_button = QPushButton("Player Settings")
        player_settings_button.setStyleSheet(BUTTON_STYLE)
        player_settings_button.clicked.connect(self.show_player_settings)
        self.layout().addWidget(player_settings_button, stretch=1)

        play_button = QPushButton("Play Game")
        play_button.setStyleSheet(BUTTON_STYLE)
        play_button.clicked.connect(self.play_game)
        self.layout().addWidget(play_button, stretch=1)

        # Spacer
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout().addItem(spacer_bottom)

    def show_map_settings(self):
        self.main_menu.show_map_settings()

    def show_player_settings(self):
        self.main_menu.show_player_settings()

    def play_game(self):
        self.main_menu.play_game()
