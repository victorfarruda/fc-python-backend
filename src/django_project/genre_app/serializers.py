from rest_framework import serializers


class GenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class ListOutputMetaSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()


class ListGenreOutputSerializer(serializers.Serializer):
    data = GenreOutputSerializer(many=True)
    meta = ListOutputMetaSerializer()


class RetrieveGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class RetrieveGenreOutputSerializer(serializers.Serializer):
    data = GenreOutputSerializer(source="*")


class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))


class CreateGenreInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True)
    categories = SetField(child=serializers.UUIDField())


class CreateGenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class UpdateGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField()
    categories_id = SetField(child=serializers.UUIDField(), required=False)


class DeleteGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class PartialUpdateGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False, required=False)
    is_active = serializers.BooleanField(required=False)
    categories_id = SetField(child=serializers.UUIDField(), required=False)
