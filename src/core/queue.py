import json

from pathlib import Path

from src.models.episode import (
    Episode,
    Section
)


class JsonQueue:


    def __init__(self, folder):

        self.folder = Path(folder)


    def get_files(self):

        return sorted(
            self.folder.glob("*.json")
        )


    def load_episode(self, file):

        data = json.loads(

            file.read_text(

                encoding="utf8"

            )

        )


        sections=[]


        for item in data["sections"]:

            sections.append(

                Section(

                    index=item["index"],

                    text=item["persian"],

                    english=item.get(
                        "english",
                        ""
                    ),

                    audio_url=item.get(
                        "audioUrl",
                        ""
                    )

                )

            )


        filename=data["metadata"]["fileName"]


        episode_id = (

            filename

            .replace(
                ".srt",
                ""
            )

        )


        return Episode(

            episode_id=episode_id,

            sections=sections,

            total_sections=len(sections)

        )