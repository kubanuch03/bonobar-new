from rest_framework import serializers

from .models import Menu
from validators.validator import validate_category_subcategory


class MenuSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%dT%H:%M:%S')

    class Meta:
        model = Menu
        fields = '__all__'

    def validate(self, data):
        return validate_category_subcategory(data)
