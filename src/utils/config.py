from pathlib import Path
import yaml
import json



class Config:


    def __init__(self):


        self.root = Path(__file__).resolve().parents[2]


        self.cfg = {}

        self.data = {}

        self.voices = {}

        self.dictionary = {}





    def load(

            self,

            path="config/config.yaml"

    ):


        self.cfg = self.load_yaml(

            path

        )


        self.data = self.cfg



        self.voices = self.load_yaml(

            "config/voices.yaml"

        )



        self.dictionary = self.load_json(

            "config/dictionary.json"

        )



        print(

            "CONFIG LOADED:"

        )


        print(

            self.cfg.keys()

        )



        return self.cfg







    def load_yaml(

            self,

            relative

    ):



        full_path = self.root / relative



        if not full_path.exists():

            raise FileNotFoundError(

                f"Config file not found: {full_path}"

            )



        with open(

                full_path,

                "r",

                encoding="utf8"

        ) as f:


            return yaml.safe_load(f)







    def load_json(

            self,

            relative

    ):



        full_path = self.root / relative



        if not full_path.exists():

            return {}



        with open(

                full_path,

                "r",

                encoding="utf8"

        ) as f:


            return json.load(f)







    def __getitem__(

            self,

            key

    ):


        return self.cfg[key]







    def get(

            self,

            *keys

    ):


        value = self.cfg



        for key in keys:


            value = value[key]



        return value







    def get_optional(

            self,

            *keys,

            default=None

    ):



        value = self.cfg



        try:


            for key in keys:


                value = value[key]



            return value



        except (

            KeyError,

            TypeError

        ):


            return default







    @property

    def input_dir(self):


        return (

            self.root /

            self.get(

                "project",

                "input_folder"

            )

        )







    @property

    def output_dir(self):


        return (

            self.root /

            self.get(

                "project",

                "output_folder"

            )

        )







    @property

    def temp_dir(self):


        return (

            self.root /

            self.get(

                "project",

                "temp_folder"

            )

        )







    @property

    def checkpoint_dir(self):


        return (

            self.root /

            self.get_optional(

                "project",

                "checkpoint_folder",

                default="checkpoint"

            )

        )







    @property

    def audio_format(self):


        return self.get_optional(

            "audio",

            "format",

            default="mp3"

        )







    @property

    def audio_bitrate(self):


        return self.get_optional(

            "audio",

            "bitrate",

            default="192k"

        )







    @property

    def log_dir(self):


        return (

            self.root /

            self.get_optional(

                "project",

                "logs",

                default="logs"

            )

        )







    def active_voice(self):


        name = self.voices.get(

            "default"

        )



        if not name:


            raise RuntimeError(

                "Default voice not defined."

            )



        voices = self.voices.get(

            "voices",

            {}

        )



        if name not in voices:


            raise RuntimeError(

                f"Voice not found: {name}"

            )



        return voices[name]