from typing import get_args

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QCheckBox, QSizePolicy
from PySide6.QtGui import QFont
from src.GUI.styles import WidgetBackgroundImage, MAIN_MENU_BACKGROUND, BUTTON_STYLE, CustomFloatSlider, \
    SelectiveWidget, CustomSequenceSlider
from src.game_control.constants import CAR_CHANGEABLE_VALUES, AI_MODES, FPS
from src.game_control.game_controller import GameController, CarAIDataHolder


class PlayerSettingsPage(WidgetBackgroundImage):
    def __init__(self, game_controller: GameController, parent, main_window):
        super(PlayerSettingsPage, self).__init__(MAIN_MENU_BACKGROUND, parent)
        self.game_controller = game_controller
        self.main_window = main_window
        self.player_widgets = []
        self.players_data_holders = [game_controller.player] + game_controller.ai_players
        self.selected_player = 0
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        # Player and AI list
        player_list_layout = QVBoxLayout()
        for i, player in enumerate(self.players_data_holders):
            if isinstance(player, CarAIDataHolder):
                active = player.active
            else:
                active = True

            player_widget = SelectiveWidget(player.name, player.image, i, active=active, mode="fit")
            player_widget.setParent(self)
            player_widget.clicked.connect(self.save_update_selection)
            player_list_layout.addWidget(player_widget)
            self.player_widgets.append(player_widget)

        player_list_container = QFrame()
        player_list_container.setLayout(player_list_layout)
        player_list_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(player_list_container, 1)

        # Vertical line
        vr_line = QFrame()
        vr_line.setFrameShape(QFrame.VLine)
        vr_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(vr_line)

        # Selected player settings
        player_settings_layout = QVBoxLayout()
        self.player_info_label = QLabel(self.players_data_holders[self.selected_player].name)
        self.player_info_label.setFont(QFont('Arial', 18, weight=QFont.Bold))
        self.player_info_label.setStyleSheet("color: white;")
        player_settings_layout.addWidget(self.player_info_label)

        self.speed_slider = CustomSequenceSlider("Max Speed", CAR_CHANGEABLE_VALUES["max_speed"])
        player_settings_layout.addWidget(self.speed_slider)

        self.acceleration_slider = CustomSequenceSlider("Acceleration", CAR_CHANGEABLE_VALUES["acceleration"])
        player_settings_layout.addWidget(self.acceleration_slider)

        self.size_slider = CustomSequenceSlider("Size", CAR_CHANGEABLE_VALUES["width_height"])
        player_settings_layout.addWidget(self.size_slider)

        self.turning_slider = CustomSequenceSlider("Turning", CAR_CHANGEABLE_VALUES["turn_speed"])
        player_settings_layout.addWidget(self.turning_slider)

        self.inactive_slider = CustomSequenceSlider("Inactive seconds after hitting", [frames // FPS for frames in CAR_CHANGEABLE_VALUES["inactive_steps"]])
        player_settings_layout.addWidget(self.inactive_slider)

        # AI Mode settings
        self.ai_mode_label = QLabel("AI Mode:")
        self.ai_mode_label.setFont(QFont('Arial', 12, weight=QFont.Bold))
        self.ai_mode_label.setStyleSheet("color: white;")
        player_settings_layout.addWidget(self.ai_mode_label)

        self.ai_mode_slider = CustomSequenceSlider("AI Mode", list(get_args(AI_MODES)))  # Assuming 0: easy, 1: medium, 2: hard
        player_settings_layout.addWidget(self.ai_mode_slider)

        # AI Active/Inactive Switch
        self.ai_active_checkbox = QCheckBox("AI Active")
        self.ai_active_checkbox.setStyleSheet("color: white;")
        self.ai_active_checkbox.setFont(QFont('Arial', 12, weight=QFont.Bold))
        self.ai_active_checkbox.stateChanged.connect(self.toggle_visibility)
        player_settings_layout.addWidget(self.ai_active_checkbox)

        # Save button
        save_button = QPushButton("Save")
        save_button.setStyleSheet(BUTTON_STYLE)
        save_button.clicked.connect(self.show_main_menu)
        player_settings_layout.addWidget(save_button)

        player_settings_container = QFrame()
        player_settings_container.setLayout(player_settings_layout)
        player_settings_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(player_settings_container, 1)

        self.setLayout(layout)

        self.update_selection(0)

    def show_main_menu(self):
        self.save_settings()
        self.main_window.show_main_menu()

    def save_update_selection(self, index: int):
        self.save_settings()
        self.update_selection(index)

    def update_selection(self, index: int):
        self.selected_player = index

        player = self.players_data_holders[index]
        is_ai = isinstance(player, CarAIDataHolder)
        self.speed_slider.set_value(player.max_speed)
        self.acceleration_slider.set_value(player.acceleration)
        self.size_slider.set_value((player.width, player.height))
        self.turning_slider.set_value(player.turn_speed)
        self.inactive_slider.set_value(player.inactive_steps // FPS)

        if is_ai:
            self.ai_mode_slider.set_value(player.mode)
            self.ai_active_checkbox.setChecked(player.active)
            self.toggle_visibility()
        else:
            self.toggle_visibility(True)

        self.toggle_ai_settings_visibility(is_ai)

        for player_widget in self.player_widgets:
            if player_widget.index == index:
                player_widget.set_selected(True)
                self.game_controller.selected_player = index
                self.player_info_label.setText(player_widget.name)
            else:
                player_widget.set_selected(False)

    def save_settings(self):
        player = self.players_data_holders[self.selected_player]
        player.max_speed = self.speed_slider.get_value()
        player.acceleration = self.acceleration_slider.get_value()
        player.width, player.height = self.size_slider.get_value()
        player.turn_speed = self.turning_slider.get_value()
        player.inactive_steps = self.inactive_slider.get_value() * FPS

        if isinstance(player, CarAIDataHolder):
            player.mode = self.ai_mode_slider.get_value()
            player.active = self.ai_active_checkbox.isChecked()

    def toggle_ai_settings_visibility(self, visible: bool):
        self.ai_mode_label.setVisible(visible)
        self.ai_mode_slider.setVisible(visible)
        self.ai_active_checkbox.setVisible(visible)

    def toggle_visibility(self, visible: bool | None = None):
        ai_active = self.ai_active_checkbox.isChecked() if visible is None else visible
        self.player_widgets[self.selected_player].active = ai_active
        self.player_widgets[self.selected_player].update()
        self.speed_slider.setEnabled(ai_active)
        self.acceleration_slider.setEnabled(ai_active)
        self.size_slider.setEnabled(ai_active)
        self.turning_slider.setEnabled(ai_active)
        self.inactive_slider.setEnabled(ai_active)
        self.ai_mode_slider.setEnabled(ai_active)