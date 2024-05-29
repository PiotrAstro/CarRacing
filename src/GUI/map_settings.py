from pathlib import Path

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtGui import QFont
from src.GUI.styles import WidgetBackgroundImage, MAIN_MENU_BACKGROUND, BUTTON_STYLE, CustomFloatSlider, SelectiveWidget
from src.game_control.constants import MAPS, LAPS_RANGE, FPS

from src.game_control.game_controller import GameController


class MapSettingsPage(WidgetBackgroundImage):
    def __init__(self, game_controller: GameController, parent, main_window):
        super(MapSettingsPage, self).__init__(MAIN_MENU_BACKGROUND, parent)
        self.game_controller = game_controller
        self.main_window = main_window
        self.map_widgets = []
        self.selected_map = 0
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Other maps list without scroll area
        map_list_layout = QHBoxLayout()
        other_maps = self.game_controller.get_all_maps()  # List of tuples (map_name, map_image_path)
        for i, (map_name, map_image_path) in enumerate(other_maps):
            map_widget = SelectiveWidget(map_name, map_image_path, i)
            map_widget.setParent(self)
            map_widget.clicked.connect(self.update_selection)
            map_list_layout.addWidget(map_widget)
            self.map_widgets.append(map_widget)

        layout.addLayout(map_list_layout)

        # Horizontal line
        hr_line = QFrame()
        hr_line.setFrameShape(QFrame.HLine)
        hr_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(hr_line)

        # Selected map info and settings
        map_info_layout = QVBoxLayout()
        self.map_info_label = QLabel(f"Map: {self.game_controller.get_map_name()}")
        self.map_info_label.setFont(QFont('Arial', 18, weight=QFont.Bold))
        self.map_info_label.setStyleSheet("color: white;")
        map_info_layout.addWidget(self.map_info_label)

        self.laps_slider = CustomFloatSlider("Laps", LAPS_RANGE[0], LAPS_RANGE[1], 1)
        map_info_layout.addWidget(self.laps_slider)

        self.time_slider = CustomFloatSlider("Time (seconds)", 10, 300, 10)
        map_info_layout.addWidget(self.time_slider)

        # Save button
        save_button = QPushButton("Save")
        save_button.setStyleSheet(BUTTON_STYLE)
        save_button.clicked.connect(self.save_settings)
        map_info_layout.addWidget(save_button)

        layout.addLayout(map_info_layout)
        self.setLayout(layout)

    def save_settings(self):
        self.game_controller.set_max_laps(self.laps_slider.get_value())
        self.game_controller.set_max_timesteps(self.time_slider.get_value() * FPS)

    def update_selection(self, index: int):
        for map_widget in self.map_widgets:
            if map_widget.index == index:
                map_widget.set_selected(True)
                self.game_controller.set_map(index)
                self.map_info_label.setText(f"Map: {map_widget.name}")

                if MAPS[index]["start_before_end_line"]:
                    self.laps_slider.update_range(LAPS_RANGE[0], LAPS_RANGE[1])
                else:
                    self.laps_slider.update_range(1, 1)
            else:
                map_widget.set_selected(False)