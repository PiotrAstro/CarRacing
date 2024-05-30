import os
from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, QPainter, Qt, QColor, QPainterPath, QBrush, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider

IMAGES_GUI_DIR = Path("images")

MAIN_MENU_BACKGROUND = IMAGES_GUI_DIR / "main_background.jpg"

BUTTON_STYLE = """
    QPushButton {
        font-size: 24px;
        color: white;
        background-color: #333;
        border: 1px solid #555;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #444;
    }
    QPushButton:pressed {
        background-color: #555;
    }
"""


class WidgetBackgroundImage(QWidget):
    def __init__(self, background_image_path, parent=None, alpha_overlay=0.5):
        super(WidgetBackgroundImage, self).__init__(parent)
        self.background_image_path = str(background_image_path)
        self.pixmap = QPixmap(self.background_image_path)
        self.alpha_overlay = alpha_overlay

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # Calculate the aspect ratio and draw the image to keep its aspect ratio
        rect = self.rect()
        image_size = self.pixmap.size()
        image_aspect_ratio = image_size.width() / image_size.height()
        widget_aspect_ratio = rect.width() / rect.height()

        if widget_aspect_ratio > image_aspect_ratio:
            # Widget is wider than image aspect ratio
            scaled_width = rect.width()
            scaled_height = scaled_width / image_aspect_ratio
        else:
            # Widget is taller than image aspect ratio
            scaled_height = rect.height()
            scaled_width = scaled_height * image_aspect_ratio

        x = int((rect.width() - scaled_width) / 2)
        y = int((rect.height() - scaled_height) / 2)

        painter.drawPixmap(x, y, scaled_width, scaled_height, self.pixmap)

        # draw dark colour overlay
        painter.fillRect(rect, QColor(0, 0, 0, int(255 * self.alpha_overlay)))




class CustomFloatSlider(QWidget):
    def __init__(self, label: str, min_value: float, max_value: float, step: float = 1.0, parent=None):
        super(CustomFloatSlider, self).__init__(parent)
        self.label_text = label
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.label = QLabel(f"{self.label_text}: {self.min_value:.2f}")
        self.update_label(self.min_value)
        self.label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(self.label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(int((self.max_value - self.min_value) / self.step))
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.update_label)
        layout.addWidget(self.slider)

    def update_label(self, value):
        value = self.min_value + value * self.step
        if float(value).is_integer():
            self.label.setText(f"{self.label_text}: {int(value)}")
        else:
            self.label.setText(f"{self.label_text}: {value:.2f}")

    def get_value(self):
        value = self.slider.value()
        return self.min_value + value * self.step

    def update_range(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        self.slider.setMaximum(int((self.max_value - self.min_value) / self.step))
        self.update_label(self.slider.value())
        if min_value == max_value:
            self.slider.setDisabled(True)
        else:
            self.slider.setDisabled(False)

    def set_value(self, value):
        self.slider.setValue(int((value - self.min_value) / self.step))
        # self.update_label(value)


class SelectiveWidget(QWidget):
    name: str
    index: int
    clicked = Signal(int)

    def __init__(self, name: str, image_path: Path | str, index: int, parent=None):
        super(SelectiveWidget, self).__init__(parent)
        self.name = name
        self.image_path = image_path
        self.pixmap = QPixmap(image_path)
        self.index = index
        self.is_selected = False
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(rect, 15, 15)
        painter.setClipPath(path)

        # Draw solid background color
        painter.setBrush(QBrush(QColor(50, 50, 50, 100)))  # Background color (dark gray)
        painter.drawRoundedRect(rect, 15, 15)

        # Calculate the size to maintain aspect ratio and crop the pixmap to fill the area
        image_size = self.pixmap.size()
        image_aspect_ratio = image_size.width() / image_size.height()
        widget_aspect_ratio = rect.width() / rect.height()

        if widget_aspect_ratio > image_aspect_ratio:
            # Widget is wider than image aspect ratio
            scaled_width = rect.width()
            scaled_height = scaled_width / image_aspect_ratio
        else:
            # Widget is taller than image aspect ratio
            scaled_height = rect.height()
            scaled_width = scaled_height * image_aspect_ratio

        x = int((rect.width() - scaled_width) / 2)
        y = int((rect.height() - scaled_height) / 2)

        painter.drawPixmap(x, y, scaled_width, scaled_height, self.pixmap)
        # painter.drawPixmap(rect, cropped_pixmap)

        # Draw semi-transparent overlay on hover and selection
        painter.setClipping(False)
        if self.is_selected:
            painter.setBrush(QColor(180, 100, 80, 100))
        elif self.underMouse():
            painter.setBrush(QColor(128, 128, 128, 100))
        else:
            painter.setBrush(Qt.transparent)

        painter.drawRoundedRect(rect, 15, 15)

        # Draw map name
        painter.setPen(Qt.white)
        painter.setFont(QFont('Arial', 16, weight=QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, self.name)

    def mousePressEvent(self, event):
        self.clicked.emit(self.index)
        self.update()

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def set_selected(self, selected: bool):
        self.is_selected = selected
        self.update()
