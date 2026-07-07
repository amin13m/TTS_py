import json

from pathlib import Path



class Checkpoint:


    def __init__(

            self,

            folder="checkpoint"

    ):

        self.folder=Path(folder)

        self.folder.mkdir(

            exist_ok=True

        )



    def file(self,episode):

        return self.folder / (

            episode + ".json"

        )



    def load(self,episode):

        f=self.file(episode)


        if not f.exists():

            return {}


        return json.loads(

            f.read_text(

                encoding="utf8"

            )

        )



    def save(

            self,

            episode,

            data

    ):

        self.file(

            episode

        ).write_text(

            json.dumps(

                data,

                ensure_ascii=False,

                indent=2

            ),

            encoding="utf8"

        )



    def mark_done(

            self,

            episode,

            section

    ):

        data=self.load(

            episode

        )


        done=data.get(

            "completed",

            []

        )


        if section not in done:

            done.append(section)



        data["completed"]=done


        self.save(

            episode,

            data

        )