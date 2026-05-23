from dataclasses import dataclass


@dataclass
class Notification:
    def __init__(self):
        self._errors = []

    def add_error(self, message: str):
        self._errors.append(message)

    @property
    def has_errors(self):
        return bool(self._errors)

    @property
    def messages(self) -> str:
        return ",".join(self._errors)
