from pathlib import Path


class VoiceManager:

    def __init__(self, config):

        self.cfg = config

        self.voices = config.voices["voices"]

    def get(self, name=None):

        if name is None or name == "":

            name = self.cfg.get("voice", "active")

        if name not in self.voices:

            raise Exception(f"Voice '{name}' not found.")

        voice = self.voices[name]

        folder = Path(voice["path"])

        ref_audio = folder / voice["audio"]

        ref_text = folder / voice["text"]

        if not ref_audio.exists():

            raise FileNotFoundError(ref_audio)

        if not ref_text.exists():

            raise FileNotFoundError(ref_text)

        with open(

                ref_text,

                encoding="utf8"

        ) as f:

            txt = f.read().strip()

        return {

            "audio": str(ref_audio),

            "text": txt,

            "speed": voice.get("speed",1.0)

        }