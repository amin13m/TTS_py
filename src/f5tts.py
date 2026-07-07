from pathlib import Path
import soundfile as sf

from f5_tts.api import F5TTS


class F5Engine:

    def __init__(self, cfg):

        self.cfg = cfg

        self.tts = None

        self.voice = cfg.voice()

        self.ref_audio = self.voice["wav"]

        self.ref_text = self.voice["text"]

    def load(self):

        print("Loading F5-TTS...")

        self.tts = F5TTS(

            model="F5TTS_v1_Base",

            device=self.cfg.get("system", "device")

        )

        print("F5 Loaded.")

    def generate(

            self,

            text,

            output_wav

    ):

        wav, sr, _ = self.tts.infer(

            ref_file=self.ref_audio,

            ref_text=self.ref_text,

            gen_text=text

        )

        sf.write(

            output_wav,

            wav,

            sr

        )

        return output_wav