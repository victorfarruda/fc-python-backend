from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.application.use_cases.create_video_without_media import (
    CreateVideoWithoutMedia,
)
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video_repository import VideoRepository


@pytest.fixture
def video_repository() -> VideoRepository:
    return MagicMock(spec=VideoRepository)


@pytest.fixture
def cast_member_repository() -> CastMemberRepository:
    return MagicMock(spec=CastMemberRepository)


@pytest.fixture
def category_repository() -> CategoryRepository:
    return MagicMock(spec=CategoryRepository)


@pytest.fixture
def genre_repository() -> GenreRepository:
    return MagicMock(spec=GenreRepository)


@pytest.fixture
def create_video_without_media(
    video_repository: VideoRepository,
    cast_member_repository: CastMemberRepository,
    category_repository: CategoryRepository,
    genre_repository: GenreRepository,
) -> CreateVideoWithoutMedia:
    return CreateVideoWithoutMedia(
        video_repository, category_repository, genre_repository, cast_member_repository
    )


class TestCreateVideoWithoutMedia:
    def test_create_video_without_media(
        self,
        create_video_without_media: CreateVideoWithoutMedia,
        video_repository: VideoRepository,
    ):
        output = create_video_without_media.execute(
            CreateVideoWithoutMedia.Input(
                title="Test Video",
                description="A video without media",
                launch_year=2024,
                duration=Decimal(120),
                rating=Rating.AGE_10.name,
                categories_id=set(),
                genres_id=set(),
                cast_members_id=set(),
            )
        )

        assert output.id is not None
        video_repository.save.assert_called_once()

    def test_create_video_without_media_with_invalid_data(
        self, create_video_without_media: CreateVideoWithoutMedia
    ):
        with pytest.raises(InvalidVideo, match="Title is required"):
            create_video_without_media.execute(
                CreateVideoWithoutMedia.Input(
                    title="",
                    description="",
                    launch_year=2024,
                    duration=Decimal(120),
                    rating=Rating.AGE_10.name,
                    categories_id=set(),
                    genres_id=set(),
                    cast_members_id=set(),
                )
            )

    def test_create_video_without_media_with_invalid_categories(
        self, create_video_without_media: CreateVideoWithoutMedia
    ):
        with pytest.raises(
            RelatedEntitiesNotFound, match="One or more categories do not exist"
        ):
            create_video_without_media.execute(
                CreateVideoWithoutMedia.Input(
                    title="Test Video",
                    description="A video without media",
                    launch_year=2024,
                    duration=Decimal(120),
                    rating=Rating.AGE_10.name,
                    categories_id={uuid4()},
                    genres_id=set(),
                    cast_members_id=set(),
                )
            )

    def test_create_video_without_media_with_invalid_genres(
        self, create_video_without_media: CreateVideoWithoutMedia
    ):
        with pytest.raises(
            RelatedEntitiesNotFound, match="One or more genres do not exist"
        ):
            create_video_without_media.execute(
                CreateVideoWithoutMedia.Input(
                    title="Test Video",
                    description="A video without media",
                    launch_year=2024,
                    duration=Decimal(120),
                    rating=Rating.AGE_10.name,
                    categories_id=set(),
                    genres_id={uuid4()},
                    cast_members_id=set(),
                )
            )

    def test_create_video_without_media_with_invalid_cast_members(
        self, create_video_without_media: CreateVideoWithoutMedia
    ):
        with pytest.raises(
            RelatedEntitiesNotFound, match="One or more cast members do not exist"
        ):
            create_video_without_media.execute(
                CreateVideoWithoutMedia.Input(
                    title="Test Video",
                    description="A video without media",
                    launch_year=2024,
                    duration=Decimal(120),
                    rating=Rating.AGE_10.name,
                    categories_id=set(),
                    genres_id=set(),
                    cast_members_id={uuid4()},
                )
            )

    def test_create_video_without_media_with_all_invalid_related_entities(
        self, create_video_without_media: CreateVideoWithoutMedia
    ):
        with pytest.raises(
            RelatedEntitiesNotFound,
            match=(
                r"^One or more categories do not exist,"
                r"One or more genres do not exist,"
                r"One or more cast members do not exist$"
            ),
        ):
            create_video_without_media.execute(
                CreateVideoWithoutMedia.Input(
                    title="Test Video",
                    description="A video without media",
                    launch_year=2024,
                    duration=Decimal(120),
                    rating=Rating.AGE_10.name,
                    categories_id={uuid4()},
                    genres_id={uuid4()},
                    cast_members_id={uuid4()},
                )
            )
