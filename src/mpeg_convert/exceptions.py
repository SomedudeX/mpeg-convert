class ModuleError(Exception):
    
    def __init__(
        self, 
        message: str,
        code: int = 1
    ) -> None:
        self.message = message
        self.code = code
        super().__init__()


class ArgumentsError(Exception):
    
    def __init__(
        self, 
        message: str,
        code: int = 1
    ) -> None:
        self.message = message
        self.code = code
        super().__init__()
