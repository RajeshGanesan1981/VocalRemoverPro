import subprocess
from pathlib import Path


class AudioProcessor:

    def process(self, input_file, output_folder):

        command = [
            "python",
            "-m",
            "demucs",
            "--two-stems=vocals",
            "-n",
            "htdemucs",
            "-o",
            output_folder,
            input_file,
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        output_path = (
            Path(output_folder)
            / "htdemucs"
            / Path(input_file).stem
        )

        vocals = output_path / "vocals.wav"
        instrumental = output_path / "no_vocals.wav"

        if not vocals.exists():
            raise Exception("vocals.wav was not created.")

        if not instrumental.exists():
            raise Exception("no_vocals.wav was not created.")

        song_name = Path(input_file).stem

        new_vocals = output_path / f"{song_name} - Vocals.wav"
        new_instrumental = output_path / f"{song_name} - Instrumental.wav"

        vocals.rename(new_vocals)
        instrumental.rename(new_instrumental)

        return str(new_vocals), str(new_instrumental)