from pathlib import Path

from f5_tts.api import F5TTS

from src.engine.base_engine import BaseEngine
from src.models.voice import Voice


class F5Engine(BaseEngine):

    def __init__(self):
        self.tts = None
        self.voice = None

    def load(self):
        if self.tts is not None:
            return

        self.tts = F5TTS(
            model="F5TTS_v1_Base"
        )

    def unload(self):
        self.tts = None

        try:
            import gc
            import torch

            gc.collect()

            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        except Exception:
            pass

    def prepare_voice(self, voice: Voice):
        self.voice = voice

        if not Path(self.voice.ref_audio).exists():
            raise FileNotFoundError(self.voice.ref_audio)

    def set_voice(self, ref_audio, ref_text):
        root = Path(__file__).resolve().parents[2]

        voice = Voice()

        voice.ref_audio = str(root / ref_audio)
        voice.ref_text = ref_text

        self.prepare_voice(voice)

    def generate(
        self,
        text,
        output_file,
        speed=1.0
    ):

        if self.tts is None:
            raise RuntimeError("Engine not loaded.")

        if self.voice is None:
            raise RuntimeError("Voice not selected.")

        self.tts.infer(
            ref_file=self.voice.ref_audio,
            ref_text=self.voice.ref_text,
            gen_text=text,
            speed=speed,
            file_wave=output_file,
            remove_silence=False
        )

    def set_voice(self, ref_audio, ref_text):
        root = Path(__file__).resolve().parents[2]
    
        voice = Voice(
            name="default",
            ref_audio=str(root / ref_audio),
            ref_text=ref_text,
            speed=1.0,
            language="fa"
        )
    
        self.prepare_voice(voice)