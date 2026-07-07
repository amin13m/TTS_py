from pathlib import Path
import re
import json
import math


class Utils:

    @staticmethod
    def ensure_folder(path):

        Path(path).mkdir(

            parents=True,

            exist_ok=True

        )

    @staticmethod
    def count_words(text):

        text = text.strip()

        if text == "":

            return 0

        return len(text.split())

    @staticmethod
    def normalize_space(text):

        text = text.replace("\n", " ")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def expected_duration(word_count):

        # میانگین سرعت گفتار فارسی

        words_per_minute = 145

        return (word_count / words_per_minute) * 60

    @staticmethod
    def save_json(file,data):

        with open(

                file,

                "w",

                encoding="utf8"

        ) as f:

            json.dump(

                data,

                f,

                ensure_ascii=False,

                indent=4

            )

    @staticmethod
    def load_json(file):

        with open(

                file,

                encoding="utf8"

        ) as f:

            return json.load(f)
        
    
    @staticmethod
    def clean_text(text):

        text = text.replace("\n", " ")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def count_words(text):

        return len(text.split())

    @staticmethod
    def expected_duration(words):

        # میانگین تقریبی گفتار فارسی
        # حدود 145 کلمه در دقیقه

        return (words / 145.0) * 60.0

    @staticmethod
    def safe_filename(name):

        return re.sub(
            r'[\\/:*?"<>|]',
            "_",
            name
        )


    