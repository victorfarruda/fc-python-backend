from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from src.core.video.application.exceptions import VideoNotFound
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus
from src.core.video.domain.video_repository import VideoRepository


class UploadVideo:
    def __init__(self, video_repository: VideoRepository, storage_service: AbstractStorageService):
        self.video_repository = video_repository
        self.storage_service = storage_service

    @dataclass
    class Input:
        video_id: UUID
        file_name: str
        content: bytes
        content_type: str
    
    def execute(self, input: Input):
        video = self.video_repository.get_by_id(input.video_id)
        if video is None:
            raise VideoNotFound(input.video_id)

        file_path = Path('videos') / str(input.video_id) / input.file_name
        self.storage_service.store(file_path, input.content, input.content_type)
    
        audio_video_media = AudioVideoMedia(
            check_sum=self.storage_service.calculate_checksum(input.content),
            name=input.file_name,
            raw_location=str(file_path),
            encoded_location="",
            status=MediaStatus.PENDING
        )

        video.update_video(audio_video_media)
        self.video_repository.update(video)
