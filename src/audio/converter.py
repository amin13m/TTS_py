from pathlib import Path
import subprocess
import shutil




class Converter:



    def __init__(

            self,

            ffmpeg="ffmpeg"

    ):

        self.ffmpeg = ffmpeg






    def wav_to_wav(

            self,

            wav,

            output

    ):


        wav = Path(wav)

        output = Path(output)



        if not wav.exists():

            raise FileNotFoundError(

                f"WAV file not found: {wav}"

            )



        output.parent.mkdir(

            parents=True,

            exist_ok=True

        )



        cmd = [

            self.ffmpeg,

            "-y",

            "-i",

            str(wav),

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

                "WAV conversion failed:\n"

                +

                e.stderr

            )



        return str(output)







    def wav_to_mp3(

            self,

            wav,

            mp3,

            bitrate="192k"

    ):



        wav = Path(wav)

        mp3 = Path(mp3)



        if not wav.exists():

            raise FileNotFoundError(

                f"WAV file not found: {wav}"

            )



        mp3.parent.mkdir(

            parents=True,

            exist_ok=True

        )



        cmd = [

            self.ffmpeg,

            "-y",

            "-i",

            str(wav),

            "-codec:a",

            "libmp3lame",

            "-b:a",

            bitrate,

            "-ar",

            "24000",

            "-ac",

            "1",

            str(mp3)

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

                "MP3 conversion failed:\n"

                +

                e.stderr

            )



        return str(mp3)









def convert_audio(

        wav,

        output,

        audio_format="mp3",

        bitrate="192k"

):


    audio_format = audio_format.lower()



    converter = Converter()



    if audio_format == "wav":


        return converter.wav_to_wav(

            wav,

            output

        )



    if audio_format == "mp3":


        return converter.wav_to_mp3(

            wav,

            output,

            bitrate

        )



    raise ValueError(

        f"Unsupported audio format: {audio_format}"

    )







def wav_to_mp3(

        wav,

        mp3,

        bitrate="192k"

):


    converter = Converter()



    return converter.wav_to_mp3(

        wav,

        mp3,

        bitrate

    )