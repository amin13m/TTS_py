from pathlib import Path

from preprocess import TextPreprocessor

from audio.converter import AudioConverter

from core.retry import RetryManager

from quality import QualityChecker

from whisper_check import WhisperChecker

from f5tts import F5Engine


class DubberEngine:

    def __init__(

            self,

            cfg,

            log

    ):

        self.cfg = cfg

        self.log = log

        self.pre = TextPreprocessor()

        self.converter = AudioConverter()

        self.retry = RetryManager(

            cfg.get(

                "system",

                "max_retry"

            )

        )

        self.tts = F5Engine(cfg)

        self.tts.load()

        self.whisper = WhisperChecker(

            cfg.get(

                "system",

                "whisper_model"

            ),

            cfg.get(

                "system",

                "device"

            )

        )

        self.quality = QualityChecker(

            cfg.get(

                "system",

                "duration_min_ratio"

            ),

            cfg.get(

                "system",

                "duration_max_ratio"

            ),

            cfg.get(

                "system",

                "similarity_threshold"

            )

        )

    def process_section(

            self,

            episode,

            section

    ):

        out_folder = Path(

            self.cfg.output_path

        ) / episode.file_name

        out_folder.mkdir(

            exist_ok=True

        )

        wav = out_folder / (

            f"{episode.prefix}"

            f"Dub"

            f"{section.index}.wav"

        )

        mp3 = out_folder / (

            f"{episode.prefix}"

            f"Dub"

            f"{section.index}.mp3"

        )

        text = self.pre.preprocess(

            section.persian

        )

        def callback(attempt):

            self.log.info(

                f"Section {section.index}"

                f" Retry {attempt}"

            )

            self.tts.generate(

                text,

                wav

            )

            result = self.whisper.transcribe(

                wav

            )

            duration_ok = self.quality.duration_ok(

                wav,

                text

            )

            sim_ok, score = self.quality.similarity_ok(

                text,

                result

            )

            if duration_ok and sim_ok:

                self.converter.wav_to_mp3(

                    wav,

                    mp3,

                    self.cfg.get(

                        "system",

                        "bitrate"

                    )

                )

                wav.unlink()

                return True, score

            return False, score

        ok, score = self.retry.run(

            callback

        )

        if ok:

            self.log.info(

                f"Accepted "

                f"{section.index}"

                f" score={score}"

            )

        else:

            self.log.error(

                f"Failed "

                f"{section.index}"

            )