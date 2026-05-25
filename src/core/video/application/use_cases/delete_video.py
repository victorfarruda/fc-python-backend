from dataclasses import dataclass
from uuid import UUID

from src.core.video.domain.video_repository import VideoRepository
from src.core.video.application.exceptions import VideoNotFound


class DeleteVideo:
    def __init__(self, repository: VideoRepository):
        self.repository = repository

    @dataclass
    class DeleteVideoInput:
        id: UUID

    def execute(self, input: DeleteVideoInput) -> None:
        video = self.repository.get_by_id(id=input.id)
        if video is None:
            raise VideoNotFound(f"Video with {input.id} not found")

        self.repository.delete(video.id)
