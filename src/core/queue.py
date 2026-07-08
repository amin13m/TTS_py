from pathlib import Path
import json

from src.models.episode import Episode
from src.models.section import Section


class JsonQueue:


    def __init__(self, input_folder):

        self.input_folder = Path(input_folder)

        self.input_folder.mkdir(
            parents=True,
            exist_ok=True
        )



    def get_files(self):

        return sorted(
            self.input_folder.glob("*.json"),
            key=lambda p: p.name.lower()
        )



    def load_episode(self, file):

        file = Path(file)


        try:

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)


        except Exception as e:

            raise RuntimeError(
                f"Cannot read JSON:\n{file}\n{e}"
            )



        episode_id = data.get(
            "episode_id",
            file.stem
        )



        sections_data = data.get(
            "sections",
            []
        )



        episode = Episode(

            episode_id=episode_id,

            total_sections=len(
                sections_data
            ),

            sections=[]

        )



        for item in sections_data:


            text = (

                item.get("text")

                or

                item.get("persian")

                or

                item.get("english")

                or

                ""

            )


            section = Section(

                index=int(
                    item.get(
                        "index",
                        len(episode.sections)+1
                    )
                ),

                text=text,

                start=item.get(
                    "start",
                    0
                ),

                end=item.get(
                    "end",
                    0
                )

            )


            episode.sections.append(
                section
            )



        episode.sections.sort(
            key=lambda x: x.index
        )


        return episode