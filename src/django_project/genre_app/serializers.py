from rest_framework import serializers


class GenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    categories = serializers.ListField(child=serializers.UUIDField())
    is_active = serializers.BooleanField()


class ListGenreOutputSerializer(serializers.Serializer):
    data = GenreOutputSerializer(many=True)


class RetrieveGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class RetrieveGenreOutputSerializer(serializers.Serializer):
    data = GenreOutputSerializer(source="*")


class CreateGenreInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True)


class CreateGenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField()


class DeleteGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class PartialUpdateGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False, required=False)
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
