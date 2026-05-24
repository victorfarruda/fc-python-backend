from uuid import UUID

from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


class InMemoryVideoRepository(VideoRepository):
    def __init__(self, videos=None):
        self.videos = videos or []

    def save(self, video: Video):
        self.videos.append(video)

    def get_by_id(self, id: UUID) -> Video | None:
        for video in self.videos:
            if video.id == id:
                return video

    def delete(self, id: UUID):
        video = self.get_by_id(id)
        self.videos.remove(video)

    def update(self, video: Video) -> None:
        old_video = self.get_by_id(video.id)
        if old_video:
            self.videos.remove(old_video)
            self.videos.append(video)

    def list(self):
        return [video for video in self.videos]
