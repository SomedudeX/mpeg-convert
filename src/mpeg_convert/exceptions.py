import sys


class ArgumentsError(Exception):
    """Represents an error during arguments parsing"""

    def __init__(
        self,
        message: str,
        code: int = 1
    ) -> None:
        """Initializes an ArgumentsError instance"""
        super().__init__(message)
        self.message = message
        self.code = code
        return
    
class ForceExit(Exception):
    """Represents a force exit of the program due to some reason"""
    
    def __init__(
        self,
        reason: str,
        code: int = 1
    ) -> None:
        super().__init__()
        self.code = code
        self.reason = reason
        return