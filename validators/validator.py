from rest_framework import serializers
import re
from django.core.exceptions import ValidationError


def validate_category_subcategory(data):
    category = data.get('category')
    subcategory = data.get('subcategory')

    if not category or not subcategory:
        raise serializers.ValidationError({'error': 'Both parent and subcategory fields must be provided.'})

    if subcategory.parent != category:
        raise serializers.ValidationError(
            {'error': 'The subcategory must be related to the provided parent category.'})

    return data


def validate_alphanumeric(value):
    if not re.match(r'^[a-zA-Z0-9\sа-яА-ЯёЁ]+$', value):
        raise ValidationError('Only contain alphanumeric characters and Cyrillic letters.')


def validate_alphanumeric_and_symbols(value):
    if re.match(r'^[\d\W]+$', value):
        raise serializers.ValidationError("Name cannot contain only numbers or symbols.")
    return value
