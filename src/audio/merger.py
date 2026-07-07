from pydub import AudioSegment


class Merger:

    @staticmethod

    def merge(

            files,

            output

    ):

        audio=AudioSegment.empty()

        for f in files:

            audio+=AudioSegment.from_file(f)

        audio.export(

            output,

            format="wav"

        )

        return output