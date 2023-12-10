class CNLearnWithMessage(Exception):
    "Custom exception with a message to be returned."

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.message: str = message
        self.status_code: int = status_code or 400
