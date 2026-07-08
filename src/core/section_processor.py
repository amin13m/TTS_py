from pathlib import Path


from src.core.chunker import Chunker
from src.core.retry import RetryManager


from src.audio.merger import Merger
from src.audio.converter import convert_audio
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



        root = Path.cwd()



        self.temp_folder = (

            root /

            config["project"]["temp_folder"]

        )


        self.output_folder = (

            root /

            config["project"]["output_folder"]

        )



        self.audio_format = (

            config["audio"]

            .get(

                "format",

                "mp3"

            )

            .lower()

        )



        self.audio_bitrate = (

            config["audio"]

            .get(

                "bitrate",

                "192k"

            )

        )



        ensure_dir(

            self.temp_folder

        )


        ensure_dir(

            self.output_folder

        )







    def process(

            self,

            episode,

            section,

            voice_name=None

    ):



        self.logger.info(

            f"Processing "

            f"{episode.episode_id} "

            f"section {section.index}"

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

                self.temp_folder /

                f"{episode.episode_id}_"

                f"{section.index:04}_"

                f"{i:04}.wav"

            )



            success = False

            last_result = None




            for attempt in RetryManager(

                    self.retry_count

            ):


                self.logger.info(

                    f"Generating chunk "

                    f"{i} "

                    f"attempt {attempt}"

                )



                try:



                    if output_wav.exists():

                        output_wav.unlink()



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

                        break



                    self.logger.warning(

                        f"Quality rejected: "

                        f"{result}"

                    )



                except Exception as e:



                    self.logger.warning(

                        f"Chunk generation error: "

                        f"{e}"

                    )







            if not success:



                self.logger.warning(

                    f"Using last audio for "

                    f"chunk {i}. "

                    f"Result={last_result}"

                )



                if not output_wav.exists():

                    raise RuntimeError(

                        f"Audio missing chunk {i}"

                    )



            generated_files.append(

                output_wav

            )







        merged_wav = (

            self.temp_folder /

            f"{episode.episode_id}_"

            f"{section.index:04}.wav"

        )



        Merger.merge(

            generated_files,

            merged_wav

        )







        if self.audio_format == "wav":


            final_file = (

                self.output_folder /

                f"{episode.episode_id}_"

                f"Dub_"

                f"{section.index:04}.wav"

            )



        else:



            final_file = (

                self.output_folder /

                f"{episode.episode_id}_"

                f"Dub_"

                f"{section.index:04}.mp3"

            )






        convert_audio(

            str(merged_wav),

            str(final_file),

            audio_format=self.audio_format,

            bitrate=self.audio_bitrate

        )





        self.logger.info(

            f"Section completed: "

            f"{final_file}"

        )



        return str(final_file)