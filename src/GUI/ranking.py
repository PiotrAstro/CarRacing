from typing import Literal

from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, \
    QHeaderView, QSizePolicy
from PySide6.QtCore import Qt
from src.GUI.styles import WidgetBackgroundImage, MAIN_MENU_BACKGROUND, BUTTON_STYLE, TABLE_STYLE
from src.car_simulator.car_python import CarWrapper
from src.game_control.constants import FPS
from src.game_control.game_controller import GameController


class RankingPage(WidgetBackgroundImage):
    def __init__(self, game_controller: GameController, parent=None, main_window=None):
        super(RankingPage, self).__init__(MAIN_MENU_BACKGROUND, parent, alpha_overlay=0.25)
        self.game_controller = game_controller
        self.main_menu = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("Game Break")
        self.title_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.title_label.setStyleSheet("color: white;")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Table for rankings
        self.ranking_table = QTableWidget()
        self.ranking_table.setStyleSheet(TABLE_STYLE)
        self.ranking_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ranking_table.verticalHeader().setVisible(False)  # Hide the row counter
        self.ranking_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Add the table to the main layout
        layout.addWidget(self.ranking_table)

        # Buttons
        button_layout = QHBoxLayout()

        self.back_to_game_button = QPushButton("Back to Game")
        self.back_to_game_button.setStyleSheet(BUTTON_STYLE)
        self.back_to_game_button.clicked.connect(self.main_menu.resume_game)
        button_layout.addWidget(self.back_to_game_button)

        self.back_to_main_menu_button = QPushButton("Back to Main Menu")
        self.back_to_main_menu_button.setStyleSheet(BUTTON_STYLE)
        self.back_to_main_menu_button.clicked.connect(self.main_menu.show_main_menu)
        button_layout.addWidget(self.back_to_main_menu_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def update_rankings(self, cars: list[CarWrapper], mode: Literal["brake", "finish"]):
        ranked_cars = sorted(cars, reverse=True)
        num_laps = self.game_controller.map_laps
        headers = ["Rank", "Name"] + [f"Lap {i + 1}" for i in range(num_laps)] + ["Distance"]

        self.ranking_table.setColumnCount(len(headers))
        self.ranking_table.setHorizontalHeaderLabels(headers)
        self.ranking_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ranking_table.setRowCount(len(ranked_cars))

        for i, car in enumerate(ranked_cars):
            self.ranking_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))  # Ranking Place
            self.ranking_table.setItem(i, 1, QTableWidgetItem(car.name))  # Player Name

            car_laps = car.get_laps()
            laps_str = [f"{lap / FPS:.2f}" for lap in car_laps] + ["-"] * (num_laps - len(car_laps))
            for j in range(num_laps):
                self.ranking_table.setItem(i, j + 2, QTableWidgetItem(laps_str[j]))

            self.ranking_table.setItem(i, 2 + num_laps, QTableWidgetItem(f"{car.distance:.2f}"))

        match mode:
            case "brake":
                self.title_label.setText("Game Break")
                self.back_to_game_button.setVisible(True)
            case "finish":
                self.title_label.setText("Game Finished")
                self.back_to_game_button.setVisible(False)
