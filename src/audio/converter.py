import subprocess
from pathlib import Path


from pathlib import Path
from pydub import AudioSegment


def wav_to_mp3(

        wav,

        mp3,

        bitrate="192k"

):

    audio = AudioSegment.from_wav(wav)

    audio.export(

        mp3,

        format="mp3",

        bitrate=bitrate

    )

    return mp3









class Converter:

    def __init__(self, ffmpeg="ffmpeg"):

        self.ffmpeg = ffmpeg

    def wav_to_mp3(

            self,

            wav,

            mp3,

            bitrate="192k"

    ):

        Path(mp3).parent.mkdir(

            parents=True,

            exist_ok=True

        )

        cmd = [

            self.ffmpeg,

            "-y",

            "-i",

            str(wav),

            "-codec:a",

            "libmp3lame",

            "-b:a",

            bitrate,

            str(mp3)

        ]

        subprocess.run(

            cmd,

            check=True,

            stdout=subprocess.DEVNULL,

            stderr=subprocess.DEVNULL

        )