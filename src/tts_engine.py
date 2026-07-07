from abc import ABC
from abc import abstractmethod


class TTSEngine(ABC):

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def generate(

            self,

            ref_audio,

            ref_text,

            text,

            output,

            speed

    ):
        pass