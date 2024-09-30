from rest_framework import serializers

from .models import Floor
from validators.validator import validate_alphanumeric_and_symbols


class FloorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Floor
        fields = ['id','title','created_at']

    def validate(self, attrs):
        title = attrs['title']
        if Floor.objects.filter(title=title).exists():
            raise serializers.ValidationError({"dublicate":"повторяющее значение!"})
        return attrs

    def validate_title(self, value):
        return validate_alphanumeric_and_symbols(value)
