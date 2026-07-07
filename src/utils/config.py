from pathlib import Path
import yaml
import json


class Config:

    def __init__(self):

        # ریشه پروژه:
        # D:\Projects\tts_py
        self.root = Path(__file__).resolve().parents[2]

        self.cfg = {}
        self.voices = {}
        self.dictionary = {}


    def load(self, path="config/config.yaml"):
    
        self.cfg = self.load_yaml(path)
    
        # سازگاری با کدهای قدیمی پروژه
        self.data = self.cfg
    
        self.voices = self.load_yaml("config/voices.yaml")
    
        self.dictionary = self.load_json("config/dictionary.json")
    
        print("CONFIG LOADED:")
        print(self.cfg.keys())
    
        return self.cfg


    def load_yaml(self, relative):

        full_path = self.root / relative

        with open(full_path, "r", encoding="utf8") as f:
            return yaml.safe_load(f)


    def load_json(self, relative):

        full_path = self.root / relative

        with open(full_path, "r", encoding="utf8") as f:
            return json.load(f)


    def __getitem__(self, key):

        return self.cfg[key]


    def get(self, *keys):

        value = self.cfg

        for key in keys:
            value = value[key]

        return value


    @property
    def input_dir(self):

        return self.root / self.get("audio", "input")


    @property
    def output_dir(self):

        return self.root / self.get("audio", "output")


    @property
    def temp_dir(self):

        return self.root / self.get("audio", "temp")


    @property
    def failed_dir(self):

        return self.root / self.get("audio", "failed")


    @property
    def log_dir(self):

        return self.root / self.get("project", "logs")


    @property
    def checkpoint_dir(self):

        return self.root / self.get("tts", "checkpoint")


    def active_voice(self):

        name = self.voices.get("default")

        return self.voices["voices"][name]