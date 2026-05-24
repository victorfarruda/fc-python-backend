import uuid

from django.db import models

from src.core.video.domain.value_objects import MediaStatus, Rating


class VideoModel(models.Model):
    RATING_CHOICES = [(rating.name, rating.name) for rating in Rating]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField()
    launch_year = models.IntegerField()
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    published = models.BooleanField()
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)

    categories = models.ManyToManyField("category_app.CategoryModel", related_name="videos")
    genres = models.ManyToManyField("genre_app.GenreModel", related_name="videos")
    cast_members = models.ManyToManyField(
        "cast_member_app.CastMemberModel", related_name="videos"
    )

    banner = models.OneToOneField(
        "ImageMediaModel",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="video_banner",
    )
    thumbnail = models.OneToOneField(
        "ImageMediaModel",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="video_thumbnail",
    )
    thumbnail_half = models.OneToOneField(
        "ImageMediaModel",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="video_thumbnail_half",
    )
    trailer = models.OneToOneField(
        "VideoMediaModel",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="video_trailer",
    )
    video = models.OneToOneField(
        "VideoMediaModel",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="video_file",
    )


class ImageMediaModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    checksum = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    raw_location = models.CharField(max_length=255)


class VideoMediaModel(models.Model):
    STATUS_CHOICES = [(status.name, status.name) for status in MediaStatus]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    checksum = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    raw_location = models.CharField(max_length=255)
    encoded_location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
