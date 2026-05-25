from dataclasses import dataclass
from enum import Enum, auto, unique
from uuid import UUID


@unique
class MediaStatus(Enum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()


@unique
class Rating(Enum):
    ER = auto()
    L = auto()
    AGE_10 = auto()
    AGE_12 = auto()
    AGE_14 = auto()
    AGE_16 = auto()
    AGE_18 = auto()


@dataclass(frozen=True)
class ImageMedia:
    check_sum: str
    name: str
    location: str


@dataclass(frozen=True)
class AudioVideoMedia:
    check_sum: str
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus
