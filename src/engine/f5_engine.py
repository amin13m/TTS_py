from pathlib import Path
import gc

import torch

from f5_tts.api import F5TTS

from src.engine.base_engine import BaseEngine
from src.models.voice import Voice



class F5Engine(BaseEngine):


    def __init__(self, config=None):

        super().__init__(config)

        self.tts = None



    def load(self):

        if self.loaded:
            return


        self.tts = F5TTS(

            model="F5TTS_v1_Base"

        )


        self.loaded = True



    def unload(self):

        self.tts = None

        gc.collect()


        if torch.cuda.is_available():

            torch.cuda.empty_cache()


        self.loaded = False



    def prepare_voice(

            self,

            voice: Voice

    ):


        root = Path(__file__).resolve().parents[2]


        if not Path(

            voice.ref_audio

        ).is_absolute():


            voice.ref_audio = str(

                root / voice.ref_audio

            )


        super().prepare_voice(

            voice

        )



    def generate(

            self,

            text,

            output_file,

            speed=None

    ):


        if not self.loaded:

            raise RuntimeError(

                "F5 Engine is not loaded"

            )


        if self.voice is None:

            raise RuntimeError(

                "Voice not selected"

            )


        if speed is None:

            speed = self.voice.speed



        self.tts.infer(

            ref_file=self.voice.ref_audio,

            ref_text=self.voice.ref_text,

            gen_text=text,

            speed=speed,

            file_wave=output_file,

            remove_silence=False

        )