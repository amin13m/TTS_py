import difflib

from pathlib import Path

from pydub import AudioSegment

from utils import Utils


class QualityChecker:

    def __init__(

            self,

            cfg,

            whisper,

            logger

    ):

        self.cfg=cfg

        self.whisper=whisper

        self.logger=logger

    def duration_ok(

            self,

            audio,

            text

    ):

        sound=AudioSegment.from_file(audio)

        seconds=len(sound)/1000

        expected=Utils.expected_duration(

            Utils.count_words(text)

        )

        ratio=seconds/expected

        mn=self.cfg.get(

            "quality",

            "min_duration_ratio"

        )

        mx=self.cfg.get(

            "quality",

            "max_duration_ratio"

        )

        ok=mn<=ratio<=mx

        return ok,ratio

    def similarity(

            self,

            original,

            detected

    ):

        return difflib.SequenceMatcher(

            None,

            original,

            detected

        ).ratio()

    def check(

            self,

            audio,

            original

    ):

        ok,ratio=self.duration_ok(

            audio,

            original

        )

        if not ok:

            self.logger.warning(

                f"Duration ratio={ratio:.2f}"

            )

            return False

        detected=self.whisper.transcribe(audio)

        sim=self.similarity(

            original,

            detected

        )

        self.logger.info(

            f"Similarity={sim:.3f}"

        )

        return sim>=0.90