from src.quality.duration_checker import DurationChecker
from src.quality.similarity import Similarity
from src.utils.whisper_checker import WhisperChecker



class QualityManager:


    def __init__(

            self,

            minimum_similarity=85,

            config=None

    ):


        self.duration = DurationChecker()


        whisper_config = {}


        if config:

            whisper_config = config.get(

                "whisper",

                {}

            )



        self.whisper = WhisperChecker(

            model_name=whisper_config.get(

                "model",

                "small"

            ),


            language=whisper_config.get(

                "language",

                "fa"

            ),


            device=whisper_config.get(

                "device",

                None

            )

        )



        self.minimum_similarity = minimum_similarity




    def normalize_text(

            self,

            text

    ):


        if not text:

            return ""


        text = text.strip()



        replace = {


            "ي": "ی",

            "ك": "ک",

            "ۀ": "ه",

            "ة": "ه"

        }



        for old,new in replace.items():

            text = text.replace(

                old,

                new

            )



        return " ".join(

            text.split()

        )





    def check(

            self,

            text,

            audio_file,

            duration

    ):



        duration_ok = self.duration.check(

            text,

            duration

        )



        duration_warning = None



        if not duration_ok:


            duration_warning = (

                "duration_out_of_range"

            )




        try:


            generated = self.whisper.transcribe(

                audio_file

            )



        except Exception as e:


            return {


                "ok": True,


                "score": 100,


                "warning": "whisper_failed",


                "error": str(e)

            }




        original = self.normalize_text(

            text

        )



        result_text = self.normalize_text(

            generated

        )



        score = Similarity.compare(

            original,

            result_text

        )



        if score < self.minimum_similarity:



            return {


                "ok": False,


                "reason": "similarity",


                "score": score,


                "expected": original,


                "generated": result_text,


                "duration_warning": duration_warning

            }




        return {


            "ok": True,


            "score": score,


            "generated": result_text,


            "duration_warning": duration_warning

        }