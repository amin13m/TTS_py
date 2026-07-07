from src.utils.config import Config
from src.utils.logger import create_logger

from src.core.queue import JsonQueue
from src.core.dubber import Dubber
from src.core.checkpoint import Checkpoint

from src.engine.f5_engine import F5Engine

from src.audio.normalizer import Normalizer

from src.quality.quality_manager import QualityManager

from src.core.section_processor import SectionProcessor



def main():


    logger=create_logger()



    config=Config()

    config.load(

        "config/config.yaml"

    )



    logger.info(

        "Loading F5-TTS"

    )


    engine=F5Engine()

    engine.load()
    
    voice = config.active_voice()
    
    engine.set_voice(
        voice["ref_audio"],
        voice["ref_text"]
    )



    logger.info(

        "Loading tools"

    )



    normalizer=Normalizer(

        "config/dictionary.json"

    )


    quality=QualityManager(

        minimum_similarity=

        config["quality"]["min_similarity"]

    )



    processor=SectionProcessor(

        engine,

        normalizer,

        quality,

        config.data,

        logger

    )


    checkpoint=Checkpoint()



    dubber=Dubber(

        processor,

        checkpoint,

        logger

    )



    queue=JsonQueue(

        config["project"]["input_folder"]

    )



    files=queue.get_files()



    if not files:

        logger.warning(

            "No input JSON found"

        )

        return



    for file in files:


        episode=queue.load_episode(

            file

        )


        dubber.process_episode(

            episode

        )



    engine.unload()



import time


if __name__ == "__main__":

    start_time = time.perf_counter()

    try:
        main()

    finally:
        end_time = time.perf_counter()

        elapsed = end_time - start_time

        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = elapsed % 60

        print("\n" + "=" * 60)
        print("Execution Time")
        print(f"{hours:02}:{minutes:02}:{seconds:06.3f}")
        print("=" * 60)