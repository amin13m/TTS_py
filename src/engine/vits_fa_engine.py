from pathlib import Path
import gc

import torch
import torchaudio

from TTS.utils.synthesizer import Synthesizer

from src.engine.base_engine import BaseEngine
from src.models.voice import Voice


class PersianVITSEngine(BaseEngine):


    def __init__(self, config=None):

        super().__init__(config)

        self.model = None



    def load(self):

        if self.loaded:
            return


        root = Path(__file__).resolve().parents[2]


        model_path = self.config.get(
            "tts",
            "models",
            "vits_fa",
            "model_path"
        )


        config_path = self.config.get(
            "tts",
            "models",
            "vits_fa",
            "config_path"
        )


        model_file = root / model_path

        config_file = root / config_path



        self.model = Synthesizer(

            tts_checkpoint=str(model_file),

            tts_config_path=str(config_file),

            use_cuda=torch.cuda.is_available()

        )


        self.loaded = True



    def unload(self):

        self.model = None


        gc.collect()


        if torch.cuda.is_available():

            torch.cuda.empty_cache()


        self.loaded = False



    def prepare_voice(
            self,
            voice: Voice
    ):

        # VITS تک گوینده است
        # نیازی به reference audio ندارد

        self.voice = voice



    def generate(
            self,
            text,
            output_file,
            speed=None
    ):


        if not self.loaded:

            raise RuntimeError(
                "Persian VITS model not loaded"
            )


        wav = self.model.tts(

            text

        )


        torchaudio.save(

            output_file,

            torch.tensor(wav)
            .unsqueeze(0),

            22050

        )