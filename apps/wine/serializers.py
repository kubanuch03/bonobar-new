from rest_framework import serializers

from .models import Wine
from validators.validator import validate_category_subcategory


class WineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wine
        fields = '__all__'

    def validate(self, data):
        return validate_category_subcategory(data)
