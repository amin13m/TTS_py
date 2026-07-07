from faster_whisper import WhisperModel



class WhisperChecker:


    def __init__(self):

        self.model=None



    def load(self):

        if self.model is None:

            self.model=WhisperModel(

                "small",

                device="cuda",

                compute_type="float16"

            )



    def transcribe(
            self,
            audio
    ):

        self.load()


        segments,info = self.model.transcribe(

            audio,

            language="fa"

        )


        text=""


        for s in segments:

            text+=s.text+" "


        return text.strip()