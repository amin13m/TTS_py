from pathlib import Path


class QueueManager:

    def __init__(self,input_folder):

        self.input=Path(input_folder)

    def files(self):

        return sorted(

            self.input.glob("*.json")

        )