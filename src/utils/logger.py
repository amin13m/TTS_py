from pathlib import Path
import logging


def create_logger(

        log_dir="logs",

        name="tts"

):


    log_path = Path(log_dir)


    log_path.mkdir(

        parents=True,

        exist_ok=True

    )


    logger = logging.getLogger(name)


    logger.setLevel(

        logging.INFO

    )


    logger.propagate = False



    # جلوگیری از تکرار Handler

    if logger.handlers:

        return logger



    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(message)s"

    )



    file_handler = logging.FileHandler(

        log_path / "project.log",

        encoding="utf-8"

    )


    file_handler.setFormatter(

        formatter

    )



    console_handler = logging.StreamHandler()


    console_handler.setFormatter(

        formatter

    )



    logger.addHandler(

        file_handler

    )


    logger.addHandler(

        console_handler

    )


    return logger



class Logger:


    def __init__(

            self,

            log_dir="logs"

    ):


        self.logger = create_logger(

            log_dir

        )


    def info(

            self,

            text

    ):

        self.logger.info(

            text

        )


    def warning(

            self,

            text

    ):

        self.logger.warning(

            text

        )


    def error(

            self,

            text

    ):

        self.logger.error(

            text

        )


    def debug(

            self,

            text

    ):

        self.logger.debug(

            text

        )