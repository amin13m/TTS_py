from dataclasses import dataclass, field


@dataclass
class Episode:

    episode_id: str

    total_sections: int

    sections: list = field(default_factory=list)