from pathlib import Path

import torchaudio


class AudioInfo:

    @staticmethod
    def duration(audio_file):

        audio_file = Path(audio_file)

        if not audio_file.exists():

            raise FileNotFoundError(audio_file)

        waveform, sample_rate = torchaudio.load(

            str(audio_file)

        )

        return (

            waveform.shape[1]

            / sample_rate

        )