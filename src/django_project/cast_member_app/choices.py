from django.db import models


class CastMemberType(models.TextChoices):
    ACTOR = "ACTOR", "ACTOR"
    DIRECTOR = "DIRECTOR", "DIRECTOR"
