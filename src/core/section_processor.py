from pathlib import Path

from src.core.chunker import Chunker
from src.core.retry import RetryManager

from src.audio.merger import Merger
from src.audio.converter import wav_to_mp3
from src.audio.audio_info import AudioInfo

from src.utils.helper import ensure_dir


class SectionProcessor:

    def __init__(
        self,
        engine,
        normalizer,
        quality,
        config,
        logger
    ):

        self.engine = engine
        self.normalizer = normalizer
        self.quality = quality
        self.logger = logger

        self.chunker = Chunker(
            max_words=config["chunk"]["max_words"]
        )

        self.retry_count = config["quality"]["max_retry"]

        self.temp_folder = Path(
            config["project"]["temp_folder"]
        )

        self.output_folder = Path(
            config["project"]["output_folder"]
        )

        ensure_dir(self.temp_folder)
        ensure_dir(self.output_folder)

    def process(
        self,
        episode,
        section,
        voice_name
    ):

        self.logger.info(
            f"Processing {episode.episode_id} section {section.index}"
        )

        text = self.normalizer.normalize(
            section.text
        )

        chunks = self.chunker.split(
            text
        )

        generated_files = []

        for i, chunk in enumerate(chunks):

            output_wav = (
                self.temp_folder
                / f"{episode.episode_id}_{section.index}_{i}.wav"
            )

            success = False
            last_result = None

            for attempt in RetryManager(self.retry_count):

                self.logger.info(
                    f"Generate chunk {i} attempt {attempt}"
                )

                self.engine.generate(
                    text=chunk,
                    output_file=str(output_wav)
                )

                duration = AudioInfo.duration(
                    output_wav
                )

                result = self.quality.check(
                    chunk,
                    str(output_wav),
                    duration
                )

                last_result = result

                if result["ok"]:
                    success = True
                    self.logger.info(
                        f"Chunk {i} passed quality check."
                    )
                    break

                self.logger.warning(
                    f"Chunk {i} attempt {attempt} failed: {result}"
                )

            if not success:
                self.logger.warning(
                    f"Chunk {i} did not pass quality after "
                    f"{self.retry_count} attempts. "
                    f"Using last generated audio anyway.\n"
                    f"Last quality result: {last_result}"
                )

            generated_files.append(output_wav)

        merged_wav = (
            self.temp_folder
            / f"{episode.episode_id}_{section.index}.wav"
        )

        Merger.merge(
            generated_files,
            merged_wav
        )

        final_mp3 = (
            self.output_folder
            / f"{episode.episode_id}Dub{section.index}.mp3"
        )

        wav_to_mp3(
            str(merged_wav),
            str(final_mp3)
        )

        self.logger.info(
            f"Section {section.index} saved successfully."
        )

        return str(final_mp3)