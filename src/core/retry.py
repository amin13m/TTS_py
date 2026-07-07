class RetryManager:


    def __init__(
            self,
            max_retry=3
    ):

        self.max_retry=max_retry



    def __iter__(self):

        return iter(

            range(

                1,

                self.max_retry+1

            )

        )