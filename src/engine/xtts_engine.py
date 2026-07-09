from pathlib import Path
import gc

import torch
import torchaudio

from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

from src.engine.base_engine import BaseEngine
from src.models.voice import Voice


class XTTSEngine(BaseEngine):


    def __init__(self, config=None):

        super().__init__(config)

        self.model = None
        self.xtts_config = None

        self.gpt_cond_latent = None
        self.speaker_embedding = None



    def load(self):

        if self.loaded:
            return


        root = Path(__file__).resolve().parents[2]


        model_path = self.config.get(
            "tts",
            "models",
            "xtts",
            "model_path"
        )


        model_dir = root / model_path


        if not model_dir.exists():
            raise FileNotFoundError(
                f"XTTS model folder not found: {model_dir}"
            )


        config_file = model_dir / "config.json"
        vocab_file = model_dir / "vocab.json"


        if not config_file.exists():
            raise FileNotFoundError(
                f"Missing XTTS config: {config_file}"
            )


        if not vocab_file.exists():
            raise FileNotFoundError(
                f"Missing XTTS vocab: {vocab_file}"
            )


        self.xtts_config = XttsConfig()

        if not config_file.exists():
            raise FileNotFoundError(
                f"Missing XTTS config: {config_file}"
            )
        
        
        if not vocab_file.exists():
            raise FileNotFoundError(
                f"Missing XTTS vocab: {vocab_file}"
            )
        
        
        if not (model_dir / "model.pth").exists():
            raise FileNotFoundError(
                f"Missing XTTS checkpoint: {model_dir}"
            )

        self.model = Xtts.init_from_config(
            self.xtts_config
        )


        self.model.load_checkpoint(
            self.xtts_config,
            checkpoint_dir=str(model_dir),
            vocab_path=str(vocab_file),
            eval=True
        )


        if torch.cuda.is_available():

            self.model.cuda()


        self.loaded = True




    def unload(self):

        self.model = None

        self.gpt_cond_latent = None
        self.speaker_embedding = None


        gc.collect()


        if torch.cuda.is_available():

            torch.cuda.empty_cache()


        self.loaded = False




    def prepare_voice(self, voice: Voice):


        root = Path(__file__).resolve().parents[2]


        audio = Path(
            voice.ref_audio
        )


        if not audio.is_absolute():

            audio = root / audio


        if not audio.exists():

            raise FileNotFoundError(
                f"Voice reference missing: {audio}"
            )


        voice.ref_audio = str(audio)


        super().prepare_voice(
            voice
        )


        (
            self.gpt_cond_latent,
            self.speaker_embedding
        ) = self.model.get_conditioning_latents(
            audio_path=self.voice.ref_audio
        )





    def generate(
            self,
            text,
            output_file,
            speed=None
    ):


        if not self.loaded:
            raise RuntimeError(
                "XTTS model not loaded"
            )


        if self.voice is None:
            raise RuntimeError(
                "Voice not selected"
            )


        if speed is None:

            speed = self.voice.speed



        language = self.voice.language


        # XTTS فارسی را قبول نمی‌کند
        # فعلاً برای تست از انگلیسی استفاده می‌کنیم
        if language == "fa":

            language = "en"



        result = self.model.inference(

            text=text,

            language=language,

            gpt_cond_latent=self.gpt_cond_latent,

            speaker_embedding=self.speaker_embedding,


            temperature=getattr(
                self.voice,
                "temperature",
                0.7
            ),


            repetition_penalty=getattr(
                self.voice,
                "repetition_penalty",
                2.0
            ),


            top_k=getattr(
                self.voice,
                "top_k",
                50
            ),


            top_p=getattr(
                self.voice,
                "top_p",
                0.85
            ),


            speed=speed
        )



        wav = torch.tensor(
            result["wav"]
        ).unsqueeze(0)



        torchaudio.save(

            output_file,

            wav.cpu(),

            24000

        )