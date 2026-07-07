from dataclasses import dataclass


@dataclass
class Section:

    index: int

    english: str

    persian: str

    audio_url: str = ""

    voice: str = ""

    speed: float = 1.0

    emotion: str = ""


@dataclass
class Episode:

    episode_name: str

    prefix: str

    sections: list