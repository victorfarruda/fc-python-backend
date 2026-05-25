from rest_framework import serializers


class ListOutputMetaSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()


class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))
