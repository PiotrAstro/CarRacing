import os
from pathlib import Path
from typing import Any, Literal

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
        outline: none;  /* Add this line to remove the focus border */
    }
    QPushButton:hover {
        background-color: #444;
    }
    QPushButton:pressed {
        background-color: #555;
    }
    QPushButton:focus {
        outline: none;  /* Add this line to remove the focus border */
    }
"""

TABLE_STYLE = """
    QTableWidget {
        background-color: rgba(43, 43, 43, 180);
        color: #f0f0f0;
        gridline-color: #444444;
        border-radius: 15px;
        font-size: 16x; /* Increase font size here */
    }
    QHeaderView::section {
        background-color: rgba(60, 60, 60, 180);
        color: #f0f0f0;
        padding: 4px;
        border: 1px solid #444444;
        font-size: 17px; /* Increase header font size */
    }
    QTableWidget QTableCornerButton::section {
        background-color: rgba(60, 60, 60, 180);
        border: 1px solid #444444;
    }
    QTableWidget::item {
        border-color: #444444;
    }
    QTableWidget::item:selected {
        background-color: #555555;
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


class CustomSequenceSlider(QWidget):
    def __init__(self, label: str, sequence: list[Any], parent=None):
        super(CustomSequenceSlider, self).__init__(parent)
        self.label_text = label
        self.sequence = sequence
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        value = self.sequence[0]
        value_str = str(value) if not isinstance(value, float) else f"{value:.2f}"
        self.label = QLabel(f"{self.label_text}: {value_str}")
        self.update_label(0)
        self.label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(self.label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.sequence) - 1)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.update_label)
        layout.addWidget(self.slider)

    def update_label(self, value):
        value = self.sequence[value]
        value_str = str(value) if not isinstance(value, float) else f"{value:.2f}"
        self.label.setText(f"{self.label_text}: {value_str}")

    def get_value(self):
        value = self.slider.value()
        return self.sequence[value]

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
        found_value_index = 0
        for i, seq_value in enumerate(self.sequence):
            if seq_value == value:
                found_value_index = i
                break

        self.slider.setValue(found_value_index)
        self.update_label(found_value_index)


class SelectiveWidget(QWidget):
    name: str
    index: int
    clicked = Signal(int)
    active: bool
    mode: Literal["full", "fit"]

    def __init__(self, name: str, image_path: Path | str, index: int, parent=None, active=True, mode: Literal["full", "fit"] = "full"):
        super(SelectiveWidget, self).__init__(parent)
        self.name = name
        self.mode = mode
        self.image_path = image_path
        self.pixmap = QPixmap(image_path)
        self.index = index
        self.active = active
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

        # Calculate the size to maintain aspect ratio and crop the pixmap to fill the area
        if self.mode == "full":
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
        else:
            # keep aspect ratio and fit the pixmap inside the area
            image_size = self.pixmap.size()
            image_aspect_ratio = image_size.width() / image_size.height()
            widget_aspect_ratio = rect.width() / rect.height()

            if widget_aspect_ratio > image_aspect_ratio:
                scaled_height = rect.height()
                scaled_width = scaled_height * image_aspect_ratio
            else:
                scaled_width = rect.width()
                scaled_height = scaled_width / image_aspect_ratio

            x = int((rect.width() - scaled_width) / 2)
            y = int((rect.height() - scaled_height) / 2)

            scaled_pixmap = self.pixmap.scaled(scaled_width, scaled_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(rect.x() + x, rect.y() + y, scaled_pixmap)

        # Draw semi-transparent overlay on hover and selection
        painter.setClipping(False)

        painter.setBrush(QBrush(QColor(10, 10, 10, 100)))  # Background color (dark gray)
        painter.drawRoundedRect(rect, 15, 15)

        if not self.active:
            painter.setBrush(QBrush(QColor(0, 100, 100, 100)))  # Background color (dark gray)
            painter.drawRoundedRect(rect, 15, 15)

        if self.is_selected:
            painter.setBrush(QColor(180, 100, 80, 100))
        elif self.underMouse():
            painter.setBrush(QColor(80, 80, 80, 100))
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
