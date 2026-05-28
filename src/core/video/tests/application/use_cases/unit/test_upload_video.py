from decimal import Decimal
from pathlib import Path
from unittest.mock import create_autospec
import uuid

import pytest

from src.core._shared.infra.storage.abstract_storage_service import (
    AbstractStorageService,
)
from src.core.video.application.exceptions import VideoNotFound
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


class TestUploadVideo:
    def test_upload_video_media_to_video(self):
        video = Video(
            title="Test Video",
            description="A video without media",
            launch_year=2024,
            duration=Decimal("120.0"),
            published=False,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video_repository = create_autospec(VideoRepository)
        video_repository.get_by_id.return_value = video
        mock_storage = create_autospec(AbstractStorageService)

        use_case = UploadVideo(
            video_repository=video_repository, storage_service=mock_storage
        )

        input = UploadVideo.Input(
            video_id=video.id,
            file_name="test_video.mp4",
            content=b"fake video content",
            content_type="video/mp4",
        )
        use_case.execute(input)

        mock_storage.store.assert_called_once_with(
            str(Path("videos") / str(video.id) / "test_video.mp4"),
            b"fake video content",
            "video/mp4",
        )
        video_from_repo = video_repository.get_by_id(video.id)
        assert video_from_repo is not None
        video_from_repo.video = AudioVideoMedia(
            name="test_video.mp4",
            raw_location=str(Path("videos") / str(video.id) / "test_video.mp4"),
            encoded_location="",
            status=MediaStatus.PENDING,
        )

    def test_when_video_not_found_then_raise_exception(self):
        video_repository = create_autospec(VideoRepository)
        video_repository.get_by_id.return_value = None
        mock_storage = create_autospec(AbstractStorageService)

        use_case = UploadVideo(
            video_repository=video_repository, storage_service=mock_storage
        )

        input = UploadVideo.Input(
            video_id=uuid.uuid4(),
            file_name="test_video.mp4",
            content=b"fake video content",
            content_type="video/mp4",
        )
        with pytest.raises(VideoNotFound, match=str(input.video_id)):
            use_case.execute(input)
