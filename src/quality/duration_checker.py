class DurationChecker:

    def __init__(

        self,

        min_ratio=0.55,

        max_ratio=2.20,

        words_per_minute=135

    ):

        self.min_ratio = min_ratio

        self.max_ratio = max_ratio

        self.words_per_minute = words_per_minute


    def estimate_duration(

        self,

        text

    ):

        words = len(

            text.split()

        )

        if words == 0:

            return 0.1

        return (

            words /

            self.words_per_minute

        ) * 60


    def check(

        self,

        text,

        duration

    ):

        expected = self.estimate_duration(

            text

        )

        ratio = duration / expected

        return (

            self.min_ratio <= ratio <= self.max_ratio

        )