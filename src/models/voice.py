from dataclasses import dataclass
from pathlib import Path



@dataclass
class Voice:


    # ---------- Base ----------

    name: str = "default"

    language: str = "fa"

    ref_audio: str = ""

    ref_text: str = ""

    speed: float = 1.0



    # ---------- XTTS ----------

    temperature: float = 0.75

    length_penalty: float = 1.0

    repetition_penalty: float = 2.0

    top_k: int = 50

    top_p: float = 0.85

    enable_text_splitting: bool = True



    # ---------- Future ----------

    style: str = ""

    emotion: str = ""

    speaker_id: str = ""

    seed: int = 0



    def validate(self):


        if not self.ref_audio:


            raise RuntimeError(

                "Reference audio is empty."

            )


        if not Path(

            self.ref_audio

        ).exists():


            raise FileNotFoundError(

                f"Reference audio not found: {self.ref_audio}"

            )



        if not self.ref_text.strip():


            raise RuntimeError(

                "Reference text is empty."

            )



    @classmethod
    def from_dict(

            cls,

            data

    ):


        return cls(

            name=data.get(

                "name",

                "default"

            ),


            language=data.get(

                "language",

                "fa"

            ),


            ref_audio=data.get(

                "ref_audio",

                ""

            ),


            ref_text=data.get(

                "ref_text",

                ""

            ),


            speed=float(

                data.get(

                    "speed",

                    1.0

                )

            ),


            temperature=float(

                data.get(

                    "temperature",

                    0.75

                )

            ),


            length_penalty=float(

                data.get(

                    "length_penalty",

                    1.0

                )

            ),


            repetition_penalty=float(

                data.get(

                    "repetition_penalty",

                    2.0

                )

            ),


            top_k=int(

                data.get(

                    "top_k",

                    50

                )

            ),


            top_p=float(

                data.get(

                    "top_p",

                    0.85

                )

            ),


            enable_text_splitting=bool(

                data.get(

                    "enable_text_splitting",

                    True

                )

            ),


            style=data.get(

                "style",

                ""

            ),


            emotion=data.get(

                "emotion",

                ""

            ),


            speaker_id=data.get(

                "speaker_id",

                ""

            ),


            seed=int(

                data.get(

                    "seed",

                    0

                )

            )

        )