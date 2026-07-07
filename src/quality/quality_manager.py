from src.quality.duration_checker import DurationChecker
from src.quality.similarity import Similarity
from src.quality.whisper_checker import WhisperChecker



class QualityManager:


    def __init__(
            self,
            minimum_similarity=90
    ):

        self.duration=DurationChecker()

        self.whisper=WhisperChecker()

        self.minimum_similarity=minimum_similarity



    def check(

            self,

            text,

            audio_file,

            duration

    ):


        duration_ok=self.duration.check(

            text,

            duration

        )


        if not duration_ok:

            return {

                "ok":False,

                "reason":"duration"

            }



        generated=self.whisper.transcribe(

            audio_file

        )


        score=Similarity.compare(

            text,

            generated

        )


        if score < self.minimum_similarity:

            return {

                "ok":False,

                "reason":"similarity",

                "score":score

            }



        return {

            "ok":True,

            "score":score

        }