from uuid import UUID

from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.video import Video
from src.django_project.video_app.models import VideoModel
from django.db import transaction


class DjangoORMVideoRepository(VideoRepository):
    def __init__(self, video_model: VideoModel = VideoModel):
        self.video_model = video_model

    def save(self, video: Video):
        video_model = VideoModelMapper.to_model(video)
        with transaction.atomic():
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)
            video_model.save()

    def get_by_id(self, id: UUID) -> Video | None:
        try:
            video = self.video_model.objects.get(id=id)
            return VideoModelMapper.to_entity(video)
        except self.video_model.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        self.video_model.objects.filter(id=id).delete()

    def update(self, video: Video) -> None:
        self.video_model.objects.filter(pk=video.id).update(
            name=video.name,
            type=video.type.value,
        )

    def list(self) -> list[Video]:
        return [
            VideoModelMapper.to_entity(video)
            for video in self.video_model.objects.all()
        ]


class VideoModelMapper:
    @staticmethod
    def to_model(video: Video) -> VideoModel:
        video_model = VideoModel(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            published=video.published,
            rating=video.rating.name,
        )
        return video_model

    @staticmethod
    def to_entity(video_model: VideoModel) -> Video:
        return Video(
            id=video_model.id,
            title=video_model.title,
            description=video_model.description,
            launch_year=video_model.launch_year,
            duration=video_model.duration,
            published=video_model.published,
            rating=video_model.rating,
            categories=set(video_model.categories.values_list("id", flat=True)),
            genres=set(video_model.genres.values_list("id", flat=True)),
            cast_members=set(video_model.cast_members.values_list("id", flat=True)),
        )
