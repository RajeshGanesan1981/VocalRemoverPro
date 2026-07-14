from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vocal Remover Pro")
        self.resize(900, 650)
        self.setMinimumSize(900, 650)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        logo = QLabel()

        pixmap = QPixmap("Assets/Logo.png")

        logo.setPixmap(
            pixmap.scaled(
                220,
                220,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

        logo.setAlignment(Qt.AlignCenter)

        title = QLabel("Vocal Remover Pro")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
        """)

        layout.addWidget(logo)
        layout.addWidget(title)

        self.setLayout(layout)