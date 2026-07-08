from pathlib import Path

import torch
import whisper



class WhisperChecker:


    _models = {}



    def __init__(

            self,

            model_name="small",

            language="fa",

            device=None

    ):


        self.model_name = model_name

        self.language = language



        if device is None:


            if torch.cuda.is_available():

                device = "cuda"

            else:

                device = "cpu"



        self.device = device



        key = (

            model_name,

            device

        )



        if key not in WhisperChecker._models:


            WhisperChecker._models[key] = whisper.load_model(

                model_name,

                device=device

            )



        self.model = WhisperChecker._models[key]




    def transcribe(

            self,

            audio_file

    ):


        audio_file = str(

            Path(audio_file)

        )



        use_fp16 = (

            self.device == "cuda"

        )



        result = self.model.transcribe(


            audio_file,


            language=self.language,


            fp16=use_fp16,


            verbose=False,


            condition_on_previous_text=False


        )



        return result.get(

            "text",

            ""

        ).strip()