from PySide6.QtCore import QObject, Signal

from core.processor import AudioProcessor


class Worker(QObject):

    finished = Signal(str, str)
    error = Signal(str)

    def __init__(self, input_file, output_folder):
        super().__init__()

        self.input_file = input_file
        self.output_folder = output_folder

    def run(self):
        try:
            processor = AudioProcessor()

            vocals, instrumental = processor.process(
                self.input_file,
                self.output_folder
            )

            self.finished.emit(
                vocals,
                instrumental
            )

        except Exception as e:
            self.error.emit(str(e))