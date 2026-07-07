from pathlib import Path

from pydub import AudioSegment


class AudioMerge:

    def merge(

            self,

            wavs,

            output

    ):

        audio=AudioSegment.empty()

        for wav in wavs:

            audio+=AudioSegment.from_wav(wav)

        Path(output).parent.mkdir(

            parents=True,

            exist_ok=True

        )

        audio.export(

            output,

            format="mp3",

            bitrate="192k"

        )