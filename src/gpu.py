import gc

import torch


class GPU:

    @staticmethod
    def clear():

        gc.collect()

        if torch.cuda.is_available():

            torch.cuda.empty_cache()