from rest_framework import serializers

from src.django_project.shared.serializers import ListOutputMetaSerializer, SetField


class CreateVideoInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(allow_null=True, required=False)

    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    duration = serializers.DecimalField(max_digits=10, decimal_places=2)
    published = serializers.BooleanField(default=False)
    rating = serializers.CharField()

    categories_id = SetField(child=serializers.UUIDField(), allow_empty=True)
    genres_id = SetField(child=serializers.UUIDField(), allow_empty=True)
    cast_members_id = SetField(child=serializers.UUIDField(), allow_empty=True)


class CreateVideoOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class VideoOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    duration = serializers.DecimalField(max_digits=10, decimal_places=2)
    published = serializers.BooleanField(default=False)
    rating = serializers.CharField()

    categories_id = SetField(child=serializers.UUIDField(), allow_empty=True)
    genres_id = SetField(child=serializers.UUIDField(), allow_empty=True)
    cast_members_id = SetField(child=serializers.UUIDField(), allow_empty=True)


class ListVideoOutputSerializer(serializers.Serializer):
    data = VideoOutputSerializer(many=True)
    meta = ListOutputMetaSerializer()


class DeleteVideoInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
