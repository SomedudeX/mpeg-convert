"""The base exceptions class used for catch-all errors emitted by the program"""


class BaseError(Exception):
    """An error to be emitted during the execution of the program. Should
    be customized with inheritance by each module separately. 

     + Notes -
        The program should not (intentionally) raise errors that does not 
        inherit from/belong to this class. If such errors are received by
        the program and have not been caught by any modules, there likely
        is a bug within this tool and should be reported. 
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
