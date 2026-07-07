from pathlib import Path
import logging


def create_logger():

    Path("logs").mkdir(exist_ok=True)

    logger = logging.getLogger("tts")

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(

        "%(asctime)s %(levelname)s %(message)s"

    )

    fh = logging.FileHandler(

        "logs/project.log",

        encoding="utf8"

    )

    fh.setFormatter(formatter)

    logger.addHandler(fh)

    logger.propagate = False

    return logger




class Logger:

    def __init__(self, log_dir):

        Path(log_dir).mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger("F5Dub")

        self.logger.setLevel(logging.INFO)

        if self.logger.handlers:
            return

        fmt = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            Path(log_dir) / "dubber.log",
            encoding="utf8"
        )

        file_handler.setFormatter(fmt)

        console = logging.StreamHandler()

        console.setFormatter(fmt)

        self.logger.addHandler(file_handler)

        self.logger.addHandler(console)

    def info(self, txt):
        self.logger.info(txt)

    def warning(self, txt):
        self.logger.warning(txt)

    def error(self, txt):
        self.logger.error(txt)