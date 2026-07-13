import shutil
import subprocess
import sys
from pathlib import Path


class AudioEngine:

    def __init__(self):
        pass

    def separate(
        self,
        input_file: str,
        output_folder: str,
    ):

        input_file = Path(input_file)
        output_folder = Path(output_folder)

        output_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        command = [
            sys.executable,
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

        final_vocals = (
            output_folder
            / "vocals.wav"
        )

        final_instrumental = (
            output_folder
            / "instrumental.wav"
        )

        if not vocals.exists():
            raise Exception(
                "Demucs did not generate vocals.wav"
            )

        if not no_vocals.exists():
            raise Exception(
                "Demucs did not generate no_vocals.wav"
            )

        shutil.copy2(
            vocals,
            final_vocals,
        )

        shutil.copy2(
            no_vocals,
            final_instrumental,
        )

        return (
            str(final_vocals),
            str(final_instrumental),
        )