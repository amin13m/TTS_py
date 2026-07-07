import json


class JsonReader:

    def read(

            self,

            file

    ):

        with open(

                file,

                encoding="utf8"

        ) as f:

            return json.load(f)

    def sections(

            self,

            file

    ):

        data = self.read(file)

        return data["sections"]