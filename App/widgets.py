from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QLabel


class DropArea(QLabel):

    fileDropped = Signal(str)

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)

        self.setMinimumHeight(170)

        self.setText(
            "🎵\n\n"
            "Drag & Drop Audio File Here\n\n"
            "Supported:\n"
            "MP3 • WAV • FLAC • M4A • AAC • OGG"
        )

        self.setStyleSheet("""
            QLabel{
                border:3px dashed #4A90E2;
                border-radius:12px;
                font-size:16px;
                background:#F7F9FC;
                color:#333333;
                padding:20px;
            }
        """)

    def dragEnterEvent(self, event: QDragEnterEvent):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()

        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):

        urls = event.mimeData().urls()

        if not urls:
            return

        filename = urls[0].toLocalFile()

        suffix = Path(filename).suffix.lower()

        allowed = [
            ".mp3",
            ".wav",
            ".flac",
            ".m4a",
            ".aac",
            ".ogg",
        ]

        if suffix not in allowed:
            self.setText(
                "❌ Unsupported Audio File\n\n"
                "Please choose MP3, WAV, FLAC,\n"
                "M4A, AAC or OGG."
            )
            return

        self.setText(
            "✅ Selected\n\n"
            f"{Path(filename).name}"
        )

        self.fileDropped.emit(filename)