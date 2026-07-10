from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel


class DropArea(QLabel):
    fileDropped = Signal(str)

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)

        self.setAlignment(Qt.AlignCenter)

        self.setMinimumHeight(180)

        self.setText("Drag & Drop Audio File Here")

        self.setStyleSheet("""
            QLabel{
                border:3px dashed #999;
                border-radius:12px;
                color:#666;
                font-size:18px;
                background:#fafafa;
            }

            QLabel:hover{
                border:3px dashed #3b82f6;
                background:#eef6ff;
            }
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()

        if not urls:
            return

        file_path = urls[0].toLocalFile()

        allowed = (
            ".mp3",
            ".wav",
            ".flac",
            ".m4a",
            ".aac",
            ".ogg"
        )

        if file_path.lower().endswith(allowed):
            self.setText(file_path.split("/")[-1])
            self.fileDropped.emit(file_path)
        else:
            self.setText("Unsupported Audio Format")