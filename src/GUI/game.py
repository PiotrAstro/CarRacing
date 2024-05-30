import time

from src.car_simulator.car_cython import CarDrawInfo
from src.game_control.constants import FPS
from src.game_control.game_controller import GameController

from PySide6.QtCore import QTimer, QRectF
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
        for car_info in cars_info:
            self.draw_car(painter, car_info, crop_x, crop_y)

    def draw_car(self, painter, car_info: CarDrawInfo, crop_x: int, crop_y: int):
        # Calculate car position relative to the cropped view
        car_x = car_info.x - crop_x
        car_y = car_info.y - crop_y

        # Apply inactive ratio to the car size
        car_width = car_info.width
        car_height = car_info.height

        # Calculate the current color based on the inactive ratio
        current_color = self.calculate_pulsing_color(car_info.inactive_ratio)

        # Save painter state
        painter.save()

        # Move and rotate the painter to draw the car
        painter.translate(car_x, car_y)
        painter.rotate(math.degrees(-car_info.angle_radians) + 90)

        # Draw the car as a rectangle
        rect = QRectF(-car_width / 2, -car_height / 2, car_width, car_height)
        painter.setBrush(current_color)
        painter.drawRect(rect)

        # Restore painter state
        painter.restore()

    def calculate_pulsing_color(self, inactive_ratio):
        if inactive_ratio <= 0:
            return QColor(255, 0, 0)  # Solid red

        # Calculate the pulsing interval based on the inactive ratio
        pulse_interval = inactive_ratio * 20  # Adjust the multiplier to change the pulse speed
        ratio = time.time() * FPS / pulse_interval
        phase = ratio - ratio // 1  # Ensure phase is between 0 and 1

        if phase < 0.5:
            return QColor(255, 0, 0)  # Red
        else:
            return QColor(255, 255, 255)  # White
