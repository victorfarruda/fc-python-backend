from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.application.list_entity import output_entity
from src.core._shared.entity import ListOutputMeta
from src.core.video.domain.video_repository import VideoRepository


@dataclass
class VideoOutput:
    id: UUID
    title: str
    description: str
    launch_year: int
    duration: Decimal
    published: bool
    rating: str
    categories_id: set[UUID]
    genres_id: set[UUID]
    cast_members_id: set[UUID]


class ListVideo:
    def __init__(self, repository: VideoRepository):
        self.repository = repository

    @dataclass
    class Input:
        order_by: str = ""
        current_page: int = 1
        per_page: int = 2

    @dataclass
    class Output:
        data: list[VideoOutput]
        meta: ListOutputMeta

    def execute(self, input: Input) -> Output:
        videos = self.repository.list()
        video_list = [
            VideoOutput(
                id=video.id,
                title=video.title,
                description=video.description,
                launch_year=video.launch_year,
                duration=video.duration,
                published=video.published,
                rating=video.rating,
                categories_id=video.categories,
                genres_id=video.genres,
                cast_members_id=video.cast_members,
            )
            for video in videos
        ]

        meta, paginated_videos = output_entity(input, video_list)
        return self.Output(
            data=paginated_videos,
            meta=meta,
        )
