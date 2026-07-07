from dataclasses import dataclass
from typing import List


@dataclass
class Section:

    index: int

    text: str

    english: str = ""

    audio_url: str = ""


@dataclass
class Episode:

    episode_id: str

    sections: List[Section]

    total_sections: int