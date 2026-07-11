import subprocess
import platform
from pathlib import Path

from PySide6.QtCore import Qt, QThread
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QProgressBar,
    QFileDialog,
    QMessageBox,
)

from App.widgets import DropArea
from App.worker import Worker


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.audio_file = None

        self.worker = None
        self.thread = None

        self.last_output_folder = None
        self.last_vocals = None
        self.last_instrumental = None

        self.setWindowTitle("Vocal Remover Pro")
        self.resize(700, 500)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)

        title = QLabel("🎵 Vocal Remover Pro")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        self.drop_area = DropArea()
        self.drop_area.fileDropped.connect(self.audio_selected)
        layout.addWidget(self.drop_area)

        self.browse_audio_btn = QPushButton("Browse Audio File")
        self.browse_audio_btn.setFixedHeight(40)
        self.browse_audio_btn.clicked.connect(self.open_audio)
        layout.addWidget(self.browse_audio_btn)

        folder_layout = QHBoxLayout()

        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText(
            "Select Output Folder"
        )

        self.folder_btn = QPushButton("Browse")
        self.folder_btn.clicked.connect(
            self.choose_folder
        )

        folder_layout.addWidget(self.output_edit)
        folder_layout.addWidget(self.folder_btn)

        layout.addLayout(folder_layout)

        self.start_btn = QPushButton(
            "Start Processing"
        )
        self.start_btn.setFixedHeight(45)
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(
            self.start_processing
        )

        layout.addWidget(self.start_btn)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        layout.addWidget(self.progress)

        self.open_folder_btn = QPushButton(
            "📂 Open Output Folder"
        )
        self.open_folder_btn.setFixedHeight(40)
        self.open_folder_btn.setEnabled(False)
        self.open_folder_btn.clicked.connect(
            self.open_output_folder
        )

        layout.addWidget(self.open_folder_btn)

        self.status = QLabel("Ready")
        layout.addWidget(self.status)

        self.setLayout(layout)

    def audio_selected(self, filename):

        self.audio_file = filename

        self.drop_area.setText(
            "✅ Selected\n\n"
            f"{Path(filename).name}"
        )

        if self.output_edit.text():
            self.start_btn.setEnabled(True)

    def open_audio(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.mp3 *.wav *.flac *.m4a *.aac *.ogg)"
        )

        if filename:
            self.audio_selected(filename)

    def choose_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder"
        )

        if folder:

            self.output_edit.setText(folder)

            if self.audio_file:
                self.start_btn.setEnabled(True)

    def start_processing(self):

        if not self.audio_file:

            QMessageBox.warning(
                self,
                "No Audio",
                "Please select an audio file."
            )
            return

        if not self.output_edit.text():

            QMessageBox.warning(
                self,
                "No Output Folder",
                "Please choose an output folder."
            )
            return

        self.start_btn.setEnabled(False)
        self.browse_audio_btn.setEnabled(False)
        self.folder_btn.setEnabled(False)
        self.open_folder_btn.setEnabled(False)

        self.progress.setRange(0, 0)
        self.status.setText("Processing...")

        self.thread = QThread()

        self.worker = Worker(
            self.audio_file,
            self.output_edit.text()
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.finished.connect(
            self.processing_finished
        )

        self.worker.error.connect(
            self.processing_error
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.error.connect(
            self.thread.quit
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.start()
        
    def processing_finished(self, vocals, instrumental):

        self.last_vocals = vocals
        self.last_instrumental = instrumental
        self.last_output_folder = str(Path(vocals).parent)

        self.progress.setRange(0, 100)
        self.progress.setValue(100)

        self.status.setText("Completed Successfully")

        self.start_btn.setEnabled(True)
        self.browse_audio_btn.setEnabled(True)
        self.folder_btn.setEnabled(True)
        self.open_folder_btn.setEnabled(True)

        QMessageBox.information(
            self,
            "Completed",
            "Vocal separation completed successfully.\n\n"
            "The output files have been saved."
        )

        if self.worker is not None:
            self.worker.deleteLater()
            self.worker = None

        self.thread = None

    def processing_error(self, message):

        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        self.status.setText("Processing Failed")

        self.start_btn.setEnabled(True)
        self.browse_audio_btn.setEnabled(True)
        self.folder_btn.setEnabled(True)

        QMessageBox.critical(
            self,
            "Error",
            message
        )

        if self.worker is not None:
            self.worker.deleteLater()
            self.worker = None

        self.thread = None

    def open_output_folder(self):

        if not self.last_output_folder:
            return

        try:

            if platform.system() == "Darwin":

                subprocess.run(
                    ["open", self.last_output_folder],
                    check=False
                )

            elif platform.system() == "Windows":

                subprocess.run(
                    ["explorer", self.last_output_folder],
                    check=False
                )

            else:

                subprocess.run(
                    ["xdg-open", self.last_output_folder],
                    check=False
                )

        except Exception as e:

            QMessageBox.warning(
                self,
                "Unable to Open Folder",
                str(e)
            )