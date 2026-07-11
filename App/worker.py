from PySide6.QtCore import QObject, Signal, Slot

from App.processor import AudioProcessor


class Worker(QObject):

    finished = Signal(str, str)
    error = Signal(str)

    def __init__(self, audio_file, output_folder):
        super().__init__()

        self.audio_file = audio_file
        self.output_folder = output_folder

    @Slot()
    def run(self):

        try:

            processor = AudioProcessor()

            vocals, instrumental = processor.process(
                self.audio_file,
                self.output_folder,
            )

            self.finished.emit(
                vocals,
                instrumental,
            )

        except Exception as e:

            self.error.emit(str(e))