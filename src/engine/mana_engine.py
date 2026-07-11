from pathlib import Path
import gc

import torch

from TTS.utils.synthesizer import Synthesizer

from src.engine.base_engine import BaseEngine
from src.models.voice import Voice


class ManaEngine(BaseEngine):

    def __init__(self, config=None):

        super().__init__(config)

        self.tts = None


    def load(self):

        if self.loaded:
            return


        root = Path(__file__).resolve().parents[2]

        model_dir = root / self.config.get(
            "tts",
            "models",
            "mana",
            "model_path"
        )


        checkpoint = model_dir / "model.pth"
        config = model_dir / "config.json"


        self.tts = Synthesizer(
            tts_checkpoint=str(checkpoint),
            tts_config_path=str(config),
            use_cuda=torch.cuda.is_available()
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

        self.voice = voice


    def generate(
            self,
            text,
            output_file,
            speed=None
    ):

        if not self.loaded:
            raise RuntimeError("Mana model not loaded")


        wav = self.tts.tts(text)


        self.tts.save_wav(
            wav,
            output_file
        )


    @property
    def name(self):

        return "ManaEngine"