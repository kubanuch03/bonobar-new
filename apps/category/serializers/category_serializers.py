from rest_framework import serializers

from apps.category.models import Category
from validators.validator import validate_alphanumeric_and_symbols


class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'created_at',)

    def validate_name(self, value):
        return validate_alphanumeric_and_symbols(value)

    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%dT%H:%M:%S')
