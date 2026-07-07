from pydub import AudioSegment


class AudioInfo:

    @staticmethod

    def duration(

            file

    ):

        audio=AudioSegment.from_file(file)

        return len(audio)/1000