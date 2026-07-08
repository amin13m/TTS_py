import time


from src.utils.config import Config
from src.utils.logger import create_logger


from src.engine.engine_factory import EngineFactory


from src.models.voice import Voice


from src.audio.normalizer import Normalizer


from src.quality.quality_manager import QualityManager


from src.core.queue import JsonQueue
from src.core.checkpoint import Checkpoint
from src.core.section_processor import SectionProcessor
from src.core.dubber import Dubber





def load_voice(config):


    data = config.active_voice()


    return Voice.from_dict(

        data

    )







def main():


    logger = create_logger()



    config = Config()


    config.load(

        "config/config.yaml"

    )



    engine = None



    try:


        logger.info(

            "Loading TTS Engine..."

        )



        engine = EngineFactory.create(

            config

        )



        engine.load()



        voice = load_voice(

            config

        )



        engine.set_voice(

            voice

        )



        logger.info(

            f"Engine : {engine.name}"

        )



        logger.info(

            f"Voice : {voice.name}"

        )



        normalizer = Normalizer(

            "config/dictionary.json"

        )



        quality = QualityManager(

            minimum_similarity=

            config["quality"]["min_similarity"],


            config=config.data

        )



        processor = SectionProcessor(

            engine,

            normalizer,

            quality,

            config.data,

            logger

        )



        checkpoint = Checkpoint(

            config["project"].get(

                "checkpoint_folder",

                "checkpoint"

            )

        )



        dubber = Dubber(
        
            processor,
        
            checkpoint,
        
            logger,
        
            output_folder=config["project"]["output_folder"],
        
            audio_format=config["audio"]["format"]
        
        )



        queue = JsonQueue(

            config["project"]["input_folder"]

        )



        files = queue.get_files()



        if not files:


            logger.warning(

                "No input JSON found."

            )


            return





        for file in files:



            logger.info(

                f"Processing file: {file.name}"

            )



            episode = queue.load_episode(

                file

            )



            dubber.process_episode(

                episode

            )





    finally:


        if engine is not None:


            logger.info(

                "Unloading TTS Engine..."

            )


            engine.unload()







if __name__ == "__main__":


    start = time.perf_counter()



    try:


        main()



    except Exception as e:


        print()

        print(

            "ERROR:"

        )

        print(e)



        raise



    finally:


        elapsed = time.perf_counter() - start



        h = int(

            elapsed // 3600

        )


        m = int(

            (elapsed % 3600) // 60

        )


        s = elapsed % 60



        print()

        print("=" * 60)

        print("Execution Time")

        print(

            f"{h:02}:{m:02}:{s:06.3f}"

        )

        print("=" * 60)