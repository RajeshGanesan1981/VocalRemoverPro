import shutil
import subprocess
from pathlib import Path


class AudioProcessor:

    def process(self, input_file, output_folder):

        input_file = Path(input_file)
        output_folder = Path(output_folder)

        output_folder.mkdir(parents=True, exist_ok=True)

        command = [
            "python",
            "-m",
            "demucs",
            "--two-stems=vocals",
            "-o",
            str(output_folder),
            str(input_file),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        demucs_folder = (
            output_folder
            / "htdemucs"
            / input_file.stem
        )

        vocals = demucs_folder / "vocals.wav"
        no_vocals = demucs_folder / "no_vocals.wav"

        final_vocals = output_folder / "vocals.wav"
        final_instrumental = output_folder / "instrumental.wav"

        if vocals.exists():
            shutil.copy2(vocals, final_vocals)

        if no_vocals.exists():
            shutil.copy2(no_vocals, final_instrumental)

        return (
            str(final_vocals),
            str(final_instrumental),
        )