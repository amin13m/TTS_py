import json

from pathlib import Path


class Normalizer:

    def __init__(

            self,

            dictionary_file

    ):

        self.words={}

        path=Path(dictionary_file)

        if path.exists():

            self.words=json.loads(

                path.read_text(

                    encoding="utf8"

                )

            )

    def normalize(

            self,

            text

    ):

        t=text

        for k,v in self.words.items():

            t=t.replace(k,v)

        return t