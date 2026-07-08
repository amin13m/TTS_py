from abc import ABC, abstractmethod

from src.models.voice import Voice


class BaseEngine(ABC):


    def __init__(self, config=None):

        self.config = config

        self.voice = None

        self.loaded = False



    @abstractmethod
    def load(self):
        pass



    @abstractmethod
    def unload(self):
        pass



    def prepare_voice(
            self,
            voice: Voice
    ):

        self.voice = voice



    def set_voice(
            self,
            voice: Voice
    ):

        self.prepare_voice(voice)



    @abstractmethod
    def generate(
            self,
            text,
            output_file,
            speed=None
    ):
        pass



    @property
    def name(self):

        return self.__class__.__name__



    def is_loaded(self):

        return self.loaded