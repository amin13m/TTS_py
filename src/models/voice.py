from dataclasses import dataclass


@dataclass
class Voice:

    name: str

    ref_audio: str

    ref_text: str

    speed: float = 1.0

    language: str = "fa"


    