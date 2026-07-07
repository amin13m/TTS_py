import re


class Chunker:


    def __init__(

            self,

            max_words=80

    ):

        self.max_words=max_words



    def split(self,text):

        sentences=re.split(

            r'([.!؟!؛])',

            text

        )


        result=[]

        current=""


        for part in sentences:

            current+=part


            words=current.split()


            if len(words)>=self.max_words:

                result.append(

                    current.strip()

                )

                current=""


        if current.strip():

            result.append(

                current.strip()

            )


        return result