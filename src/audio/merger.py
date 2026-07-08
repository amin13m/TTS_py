from pathlib import Path
import subprocess
import tempfile



class Merger:


    @staticmethod
    def merge(

            files,

            output,

            ffmpeg="ffmpeg"

    ):


        files = [

            Path(f)

            for f in files

        ]



        if not files:

            raise ValueError(

                "No audio files to merge"

            )



        for f in files:


            if not f.exists():


                raise FileNotFoundError(

                    f"Audio file not found: {f}"

                )



        output = Path(output)



        output.parent.mkdir(

            parents=True,

            exist_ok=True

        )




        with tempfile.NamedTemporaryFile(

                mode="w",

                suffix=".txt",

                delete=False,

                encoding="utf-8"

        ) as temp:



            list_file = temp.name



            for f in files:


                temp.write(

                    f"file '{f.resolve()}'\n"

                )





        cmd = [

            ffmpeg,

            "-y",

            "-f",

            "concat",

            "-safe",

            "0",

            "-i",

            list_file,

            "-ar",

            "24000",

            "-ac",

            "1",

            "-c:a",

            "pcm_s16le",

            str(output)

        ]



        try:


            subprocess.run(

                cmd,

                check=True,

                stdout=subprocess.PIPE,

                stderr=subprocess.PIPE,

                text=True

            )



        except subprocess.CalledProcessError as e:


            raise RuntimeError(

                "FFmpeg merge failed:\n"

                +

                e.stderr

            )



        finally:


            Path(list_file).unlink(

                missing_ok=True

            )



        return str(output)