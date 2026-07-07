import math


class DurationChecker:


    def __init__(
            self,
            min_ratio=0.65,
            max_ratio=1.8
    ):

        self.min_ratio=min_ratio

        self.max_ratio=max_ratio



    def estimate_duration(
            self,
            text,
            words_per_minute=130
    ):

        words=len(
            text.split()
        )


        minutes=words / words_per_minute


        return minutes * 60



    def check(
            self,
            text,
            duration
    ):

        expected=self.estimate_duration(text)


        ratio=duration / expected


        return (

            self.min_ratio

            <= ratio

            <= self.max_ratio

        )