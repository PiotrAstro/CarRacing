from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QComboBox, QPushButton

class MapSettingsPage(QWidget):
    def __init__(self, parent, game_controller):
        super(MapSettingsPage, self).__init__(parent)
        # self.game_controller = game_controller
        # self.layout = QVBoxLayout()
        # self.form_layout = QFormLayout()
        # self.map_combo = QComboBox()
        # self.map_combo.addItems(["Map 1", "Map 2", "Map 3"])
        # self.map_combo.setCurrentText(self.game_controller.get_map_setting())
        # self.form_layout.addRow(QLabel("Select Map"), self.map_combo)
        # self.layout.addLayout(self.form_layout)
        # self.back_button = QPushButton("Back")
        # self.back_button.clicked.connect(self.save_and_back)
        # self.layout.addWidget(self.back_button)
        # self.setLayout(self.layout)

    def save_and_back(self):
        # self.game_controller.set_map_setting(self.map_combo.currentText())
        self.parent().show_main_menu()

class PlayerSettingsPage(QWidget):
    def __init__(self, parent, game_controller):
        super(PlayerSettingsPage, self).__init__(parent)
        # self.game_controller = game_controller
        # self.layout = QVBoxLayout()
        # self.form_layout = QFormLayout()
        # self.character_combo = QComboBox()
        # self.character_combo.addItems(["Warrior", "Mage", "Archer"])
        # self.character_combo.setCurrentText(self.game_controller.get_player_settings()["Character"])
        # self.form_layout.addRow(QLabel("Character"), self.character_combo)
        # self.difficulty_combo = QComboBox()
        # self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])
        # self.difficulty_combo.setCurrentText(self.game_controller.get_player_settings()["Difficulty"])
        # self.form_layout.addRow(QLabel("Difficulty"), self.difficulty_combo)
        # self.layout.addLayout(self.form_layout)
        # self.back_button = QPushButton("Back")
        # self.back_button.clicked.connect(self.save_and_back)
        # self.layout.addWidget(self.back_button)
        # self.setLayout(self.layout)

    def save_and_back(self):
        settings = {
            "Character": self.character_combo.currentText(),
            "Difficulty": self.difficulty_combo.currentText()
        }
        # self.game_controller.set_player_settings(settings)
        self.parent().show_main_menu()

class AISettingsPage(QWidget):
    def __init__(self, parent, game_controller):
        super(AISettingsPage, self).__init__(parent)
        # self.game_controller = game_controller
        # self.layout = QVBoxLayout()
        # self.form_layout = QFormLayout()
        # self.ai_level_combo = QComboBox()
        # self.ai_level_combo.addItems(["Beginner", "Intermediate", "Expert"])
        # self.ai_level_combo.setCurrentText(self.game_controller.get_ai_setting())
        # self.form_layout.addRow(QLabel("AI Level"), self.ai_level_combo)
        # self.layout.addLayout(self.form_layout)
        # self.back_button = QPushButton("Back")
        # self.back_button.clicked.connect(self.save_and_back)
        # self.layout.addWidget(self.back_button)
        # self.setLayout(self.layout)

    def save_and_back(self):
        # self.game_controller.set_ai_setting(self.ai_level_combo.currentText())
        self.parent().show_main_menu()