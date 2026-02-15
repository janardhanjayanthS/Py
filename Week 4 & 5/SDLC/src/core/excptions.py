class WeakPasswordException(Exception):
    """Exception raised when a password does not meet strength requirements.

    Args:
        message: Description of why the password is weak.
    """

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)
