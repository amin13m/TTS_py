from pathlib import Path
import gc

import torch
import soundfile as sf

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


        print("Loading XTTS config...")


        config_file = model_dir / "config.json"
        vocab_file = model_dir / "vocab.json"
        model_file = model_dir / "model.pth"



        if not config_file.exists():
            raise FileNotFoundError(config_file)


        if not vocab_file.exists():
            raise FileNotFoundError(vocab_file)


        if not model_file.exists():
            raise FileNotFoundError(model_file)



        self.xtts_config = XttsConfig()

        self.xtts_config.load_json(
            str(config_file)
        )



        print("Initializing XTTS...")


        self.model = Xtts.init_from_config(
            self.xtts_config
        )



        print("Loading checkpoint...")


        self.model.load_checkpoint(
            self.xtts_config,
            checkpoint_dir=str(model_dir),
            vocab_path=str(vocab_file),
            eval=True
        )


        if torch.cuda.is_available():

            self.model.cuda()



        self.model.eval()


        print("XTTS loaded successfully")


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



        print(
            f"Preparing XTTS voice: {audio}"
        )



        super().prepare_voice(
            voice
        )



        with torch.no_grad():


            (
                self.gpt_cond_latent,
                self.speaker_embedding

            ) = self.model.get_conditioning_latents(

                audio_path=str(audio),

                gpt_cond_len=30,

                max_ref_length=30,

                sound_norm_refs=False

            )



        print(
            "Voice embedding ready"
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



        # XTTS v2 supported languages
        # Persian is not officially supported

        if language == "fa":

            language = "en"



        print(
            f"XTTS generating ({language}): {text[:80]}"
        )



        with torch.no_grad():


            result = self.model.inference(

                text=text,

                language=language,


                gpt_cond_latent=self.gpt_cond_latent,


                speaker_embedding=self.speaker_embedding,



                temperature=getattr(
                    self.voice,
                    "temperature",
                    0.75
                ),


                repetition_penalty=getattr(
                    self.voice,
                    "repetition_penalty",
                    5.0
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

            
        wav = result["wav"]


        # تبدیل خروجی XTTS به numpy

        if isinstance(wav, torch.Tensor):

            wav = wav.detach().cpu().numpy()



        # ذخیره مستقیم بدون TorchCodec

        sf.write(

            output_file,

            wav,

            24000,

            subtype="PCM_16"

        )



        return output_file