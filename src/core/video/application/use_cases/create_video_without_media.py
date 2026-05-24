from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.notification import Notification
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


class CreateVideoWithoutMedia:
    @dataclass
    class Input:
        title: str
        description: str
        launch_year: int
        duration: Decimal
        rating: str
        categories: set[UUID]
        genres: set[UUID]
        cast_members: set[UUID]

    @dataclass
    class Output:
        id: UUID

    def __init__(
        self,
        video_repository: VideoRepository,
        category_repository: CategoryRepository,
        genre_repository: GenreRepository,
        cast_member_repository: CastMemberRepository,
    ) -> None:
        self.video_repository = video_repository
        self.category_repository = category_repository
        self.genre_repository = genre_repository
        self.cast_member_repository = cast_member_repository
        self.notification = Notification()

    def validate_categories(self, category_ids: set[UUID]):
        categories_ids = {category.id for category in self.category_repository.list()}
        if not category_ids.issubset(categories_ids):
            self.notification.add_error("One or more categories do not exist")

    def validate_genres(self, genre_ids: set[UUID]):
        genres_ids = {genre.id for genre in self.genre_repository.list()}
        if not genre_ids.issubset(genres_ids):
            self.notification.add_error("One or more genres do not exist")

    def validate_cast_members(self, cast_member_ids: set[UUID]):
        cast_member_ids_existing = {
            cast_member.id for cast_member in self.cast_member_repository.list()
        }
        if not cast_member_ids.issubset(cast_member_ids_existing):
            self.notification.add_error("One or more cast members do not exist")

    def execute(self, input: Input) -> Output:
        self.validate_categories(input.categories)
        self.validate_genres(input.genres)
        self.validate_cast_members(input.cast_members)

        if self.notification.has_errors:
            raise RelatedEntitiesNotFound(self.notification.messages)

        try:
            video = Video(
                title=input.title,
                description=input.description,
                launch_year=input.launch_year,
                duration=input.duration,
                published=False,
                rating=Rating(input.rating),
                categories=input.categories,
                genres=input.genres,
                cast_members=input.cast_members,
            )
        except ValueError as e:
            raise InvalidVideo(str(e)) from e

        self.video_repository.save(video)
        return self.Output(id=video.id)
