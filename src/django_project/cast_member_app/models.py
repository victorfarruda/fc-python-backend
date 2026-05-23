import uuid

from django.db import models

from src.django_project.cast_member_app.choices import CastMemberType


class CastMemberModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=CastMemberType.choices)

    class Meta:
        db_table = "cast_member"

    def __str__(self):
        return f"{self.name} - {self.type}"
