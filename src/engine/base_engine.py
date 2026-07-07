from abc import ABC, abstractmethod


class BaseEngine(ABC):
    """Base class for all TTS engines."""

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def unload(self):
        pass

    @abstractmethod
    def prepare_voice(self, voice_name: str):
        pass

    @abstractmethod
    def generate(
        self,
        text: str,
        output_file: str,
        speed: float = 1.0,
    ):
        pass