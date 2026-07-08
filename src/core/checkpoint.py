import json
from pathlib import Path
from datetime import datetime




class Checkpoint:


    def __init__(

            self,

            folder="checkpoint"

    ):


        self.folder = Path(folder)



        self.folder.mkdir(

            parents=True,

            exist_ok=True

        )







    def file(

            self,

            episode

    ):


        return self.folder / f"{episode}.json"







    def load(

            self,

            episode

    ):


        path = self.file(

            episode

        )


        if not path.exists():

            return {}



        try:


            return json.loads(

                path.read_text(

                    encoding="utf-8"

                )

            )



        except Exception:


            return {}







    def save(

            self,

            episode,

            data

    ):



        path = self.file(

            episode

        )


        data["updated"] = datetime.now().isoformat()



        temp = path.with_suffix(

            ".tmp"

        )



        temp.write_text(

            json.dumps(

                data,

                ensure_ascii=False,

                indent=2

            ),

            encoding="utf-8"

        )



        temp.replace(

            path

        )








    def mark_done(

            self,

            episode,

            section,

            output=None

    ):


        data = self.load(

            episode

        )



        completed = data.get(

            "completed",

            []

        )



        if section not in completed:


            completed.append(

                section

            )



        completed.sort()



        data["completed"] = completed



        if output:


            outputs = data.get(

                "outputs",

                {}

            )


            outputs[str(section)] = output


            data["outputs"] = outputs



        self.save(

            episode,

            data

        )







    def mark_failed(

            self,

            episode,

            section,

            reason

    ):



        data = self.load(

            episode

        )



        failed = data.get(

            "failed",

            {}

        )



        failed[str(section)] = {


            "reason": reason,


            "time":

            datetime.now().isoformat()

        }



        data["failed"] = failed



        self.save(

            episode,

            data

        )