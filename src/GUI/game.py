import time
from src.car_simulator.car_cython import CarDrawInfo
from src.game_control.constants import FPS
from src.game_control.game_controller import GameController

from PySide6.QtCore import QTimer, QRectF, Qt
from PySide6.QtGui import QPainter, QColor, QPixmap, QFont
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
import math


class GamePage(QWidget):
    def __init__(self, game_controller: GameController, parent, main_window):
        super(GamePage, self).__init__(parent)
        self.game_controller = game_controller
        self.main_window = main_window
        self.game_running = False
        self.initUI()

        # Update the widget periodically based on the simulation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000 // 60)  # Update at 60 FPS

    def start_game(self):
        self.simulation = self.game_controller.create_game_simulation()
        self.cars = self.simulation.cars_ai + [self.simulation.cars_players[0]]
        self.cars_images = [QPixmap(car.image) for car in self.cars]
        self.car_names = [car.name for car in self.cars]
        self.map_pixmap = QPixmap(self.game_controller.get_map_image())
        self.game_running = True
        self.update_data()

    def initUI(self):
        # Layout for the top labels
        top_layout = QHBoxLayout()

        # Time left label
        self.time_left_label = QLabel("Time left: 0")
        self.time_left_label.setFont(QFont('Arial', 14, QFont.Bold))
        self.time_left_label.setStyleSheet("color: white;")
        top_layout.addWidget(self.time_left_label)

        # Spacer
        top_layout.addStretch()

        # Laps label
        self.laps_label = QLabel("Laps: 0")
        self.laps_label.setFont(QFont('Arial', 14, QFont.Bold))
        self.laps_label.setStyleSheet("color: white;")
        top_layout.addWidget(self.laps_label)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def update_data(self):
        if self.game_running:
            # Fetch updated simulation data
            time_left = (self.game_controller.map_max_timesteps - self.simulation.current_timestep) / FPS
            laps = self.cars[-1].get_laps()

            if len(laps) < self.game_controller.map_laps:
                # Update the simulation
                laps.append(self.simulation.current_timestep)
            laps = map(lambda x: x / FPS, laps)

            # Update labels
            self.time_left_label.setText(f"Time left: {time_left:.2f}")
            self.laps_label.setText("Laps: " + "\n".join(f"{i + 1}: {lap:.2f}" for i, lap in enumerate(laps)))

            # Redraw the widget
            self.update()

            if not self.simulation.is_finished():
                self.simulation.step()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # Calculate the region to display centered on the main car
        map_rect = self.map_pixmap.rect()
        view_width = self.width()
        view_height = self.height()
        half_view_width = view_width // 2
        half_view_height = view_height // 2

        cars_info = [car.get_car_draw_info() for car in self.cars]
        center_x = cars_info[-1].x
        center_y = cars_info[-1].y

        # Ensure the view does not go out of map boundaries
        crop_x = max(0, min(map_rect.width() - view_width, center_x - half_view_width))
        crop_y = max(0, min(map_rect.height() - view_height, center_y - half_view_height))

        # Crop and draw the map
        cropped_map = self.map_pixmap.copy(crop_x, crop_y, view_width, view_height)
        painter.drawPixmap(0, 0, cropped_map)

        # Draw the cars
        for car_info, image, name in zip(cars_info, self.cars_images, self.car_names):
            self.draw_car(painter, car_info, image, name, crop_x, crop_y)

    def draw_car(self, painter, car_info: CarDrawInfo, car_image, car_name, crop_x: int, crop_y: int):
        # Calculate car position relative to the cropped view
        car_x = car_info.x - crop_x
        car_y = car_info.y - crop_y

        # Apply inactive ratio to the car size
        car_width = car_info.width
        car_height = car_info.height

        # Calculate the current color based on the inactive ratio

        # Save painter state
        painter.save()

        painter.translate(car_x, car_y)
        pulsing_opacity = self.calculate_pulsing_opacity(car_info.inactive_ratio)

        # Draw the player name above the car
        text_width = painter.fontMetrics().horizontalAdvance(car_name)
        padding = 10  # Add padding to the width
        text_rect = QRectF(-text_width / 2 - padding / 2, -car_height / 2 - 20 - padding, text_width + padding, 20)
        painter.setOpacity(1)
        painter.setPen(
            QColor(255, 255, 255) if pulsing_opacity == 1 else QColor(255, 0, 0)
        )  # White color for text
        painter.setFont(QFont('Arial', 10, QFont.Bold))
        painter.drawText(text_rect, Qt.AlignCenter, car_name)

        # Move and rotate the painter to draw the car
        painter.rotate(math.degrees(-car_info.angle_radians))

        painter.setOpacity(pulsing_opacity)  # Adjust opacity based on inactive ratio
        painter.drawPixmap(-car_height / 2, - car_width / 2, car_height, car_width, car_image)



        # Restore painter state
        painter.restore()

    def calculate_pulsing_opacity(self, inactive_ratio) -> float:
        if inactive_ratio == 0.0:
            return 1.0

        # Calculate the pulsing interval based on the inactive ratio
        pulse_interval = 0.3  # math.sqrt(inactive_ratio) / 2  # Adjust the multiplier to change the pulse speed

        seconds = time.time()
        seconds = seconds - seconds // 1
        ratio = seconds / pulse_interval

        phase = ratio - ratio // 1  # Ensure phase is between 0 and 1

        if phase < 0.5:
            return 0.0
        else:
            return 1.0
