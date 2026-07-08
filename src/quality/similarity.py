import re

from rapidfuzz import fuzz


class Similarity:

    @staticmethod
    def normalize(text: str):

        if text is None:
            return ""

        text = text.lower()

        text = text.replace("ي", "ی")
        text = text.replace("ك", "ک")

        text = text.replace("‌", " ")

        text = re.sub(r"[^\w\s]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()


    @classmethod
    def compare(

        cls,

        original,

        generated

    ):

        original = cls.normalize(original)

        generated = cls.normalize(generated)

        if not original:

            return 0

        score = fuzz.token_sort_ratio(

            original,

            generated

        )

        return score