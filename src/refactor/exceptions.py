"""The base exceptions class"""


class BaseError(Exception):
    """An error to be emitted during the execution of the program. Should
    be customized with inheritance by each module separately. 
    """

    def __init__(
        self,
        exit_code: int
    ) -> None:
        """Initializes an instance of BaseError

         + Args - 
            exit_code: The exit code"""
        self.code = exit_code
        return
