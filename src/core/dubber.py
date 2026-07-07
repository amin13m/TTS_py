from pathlib import Path

from src.core.queue import JsonQueue
from src.core.section_processor import SectionProcessor
from src.core.checkpoint import Checkpoint



class Dubber:


    def __init__(

            self,

            processor: SectionProcessor,

            checkpoint: Checkpoint,

            logger

    ):

        self.processor = processor

        self.checkpoint = checkpoint

        self.logger = logger



    def process_episode(

            self,

            episode

    ):


        self.logger.info(

            f"Start episode: "

            f"{episode.episode_id}"

        )


        state=self.checkpoint.load(

            episode.episode_id

        )


        completed=state.get(

            "completed",

            []

        )



        outputs=[]



        for section in episode.sections:


            if section.index in completed:


                self.logger.info(

                    f"Skip section "

                    f"{section.index}"

                )

                continue



            result=self.processor.process(

                episode,

                section,

                None

            )


            outputs.append(

                result

            )


            self.checkpoint.mark_done(

                episode.episode_id,

                section.index

            )



        self.logger.info(

            f"Episode finished "

            f"{episode.episode_id}"

        )


        return outputs