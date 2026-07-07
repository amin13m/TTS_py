import json

from pathlib import Path

from models import Episode

from models import Section


class JsonReader:

    def load(self, file, prefix):

        with open(

                file,

                encoding="utf8"

        ) as f:

            data = json.load(f)

        sections = []

        for item in data["sections"]:

            section = Section(

                index=item["index"],

                english=item.get("english", ""),

                persian=item.get("persian", ""),

                audio_url=item.get("audioUrl", ""),

                voice=item.get("voice", ""),

                speed=item.get("speed", 1.0),

                emotion=item.get("emotion", "")

            )

            sections.append(section)

        return Episode(

            episode_name=Path(file).stem,

            prefix=prefix,

            sections=sections

        )