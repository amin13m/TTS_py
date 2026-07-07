from rapidfuzz.fuzz import ratio



class Similarity:


    @staticmethod

    def compare(
            original,
            generated
    ):

        return ratio(

            original,

            generated

        )