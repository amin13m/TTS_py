from pathlib import Path



class Dubber:


    def __init__(

            self,

            processor,

            checkpoint,

            logger,

            output_folder="output",

            audio_format="mp3"

    ):


        self.processor = processor

        self.checkpoint = checkpoint

        self.logger = logger



        self.output_folder = Path(

            output_folder

        )



        self.audio_format = audio_format.lower()



        self.output_folder.mkdir(

            parents=True,

            exist_ok=True

        )







    def expected_output(

            self,

            episode_id,

            section_index

    ):



        return (

            self.output_folder /

            f"{episode_id}_"

            f"Dub_"

            f"{section_index:04}."

            f"{self.audio_format}"

        )







    def process_episode(

            self,

            episode

    ):



        self.logger.info(

            "=" * 70

        )



        self.logger.info(

            f"Episode : {episode.episode_id}"

        )



        self.logger.info(

            "=" * 70

        )





        state = self.checkpoint.load(

            episode.episode_id

        )



        completed = state.get(

            "completed",

            []

        )



        outputs = []



        total = len(

            episode.sections

        )





        for index, section in enumerate(

                episode.sections,

                start=1

        ):



            self.logger.info(

                f"[{index}/{total}] "

                f"Section {section.index}"

            )



            output_file = self.expected_output(

                episode.episode_id,

                section.index

            )





            if output_file.exists():



                self.logger.info(

                    "Output already exists."

                )



                outputs.append(

                    str(output_file)

                )



                if section.index not in completed:


                    self.checkpoint.mark_done(

                        episode.episode_id,

                        section.index

                    )



                continue





            if section.index in completed:



                self.logger.warning(

                    "Checkpoint exists but output missing. Regenerating."

                )



            try:



                result = self.processor.process(

                    episode,

                    section,

                    None

                )



                outputs.append(

                    result

                )



                self.checkpoint.mark_done(

                    episode.episode_id,

                    section.index,
                    result
                )





            except Exception as e:



                self.logger.exception(

                    f"Section {section.index} failed: {e}"

                )



                continue





        self.logger.info(

            "=" * 70

        )



        self.logger.info(

            f"Episode Finished : {episode.episode_id}"

        )



        self.logger.info(

            "=" * 70

        )



        return outputs