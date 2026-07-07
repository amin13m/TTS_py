from faster_whisper import WhisperModel


class WhisperChecker:

    def __init__(

            self,

            model_name,

            device

    ):

        self.model = WhisperModel(

            model_name,

            device=device,

            compute_type="float16"

            if device == "cuda"

            else "int8"

        )

    def transcribe(

            self,

            audio

    ):

        segments, _ = self.model.transcribe(

            audio,

            language="fa"

        )

        text = ""

        for seg in segments:

            text += seg.text + " "

        return text.strip()