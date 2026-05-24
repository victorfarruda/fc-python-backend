from decimal import Decimal
from uuid import UUID, uuid4

import pytest

from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video


class TestVideo:
    def test_fields_are_required(self):
        with pytest.raises(
            TypeError,
            match=(
                r"missing 9 required positional arguments: 'title', "
                r"'description', 'launch_year', 'duration', 'published', "
                r"'rating', 'categories', 'genres', and 'cast_members'"
            ),
        ):
            Video(id=uuid4())

    def test_title_cannot_be_empty(self):
        with pytest.raises(ValueError, match="Title is required"):
            Video(
                id=uuid4(),
                title="",
                description="",
                launch_year=0,
                duration=Decimal("0.0"),
                published=False,
                rating=Rating.ER,
                categories=set(),
                genres=set(),
                cast_members=set(),
            )

    def test_can_create_video(self):
        video = Video(
            id=uuid4(),
            title="Video title",
            description="Video description",
            launch_year=2023,
            duration=Decimal("120.0"),
            published=True,
            rating=Rating.ER,
            categories={uuid4()},
            genres={uuid4()},
            cast_members={uuid4()},
        )
        assert video.title == "Video title"
        assert video.id is not None
        assert isinstance(video.id, UUID)
        assert video.description == "Video description"
        assert video.launch_year == 2023
        assert video.duration == Decimal("120.0")
        assert video.published is True
        assert video.rating == Rating.ER
        assert len(video.categories) == 1
        assert len(video.genres) == 1
        assert len(video.cast_members) == 1
