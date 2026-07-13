from PySide6.QtCore import QObject, Signal, Slot

from Engine.audio_engine import AudioEngine


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

            engine = AudioEngine()

            vocals, instrumental = engine.separate(
                self.audio_file,
                self.output_folder,
            )

            self.finished.emit(
                str(vocals),
                str(instrumental),
            )

        except Exception as e:

            self.error.emit(str(e))