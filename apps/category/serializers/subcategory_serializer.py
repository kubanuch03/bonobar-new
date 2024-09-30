from rest_framework import serializers

from ..models import SubCategory, Category
from validators.validator import validate_alphanumeric_and_symbols
from .category_serializers import CategorySerializer


class CategoryForSubCategorySerializer(CategorySerializer):

    class Meta(CategorySerializer.Meta):
        model = Category
        fields = ('id', 'name')


class SubCategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    parent_details = CategoryForSubCategorySerializer(source='parent', read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'parent', 'parent_details','order']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('parent', None)
        return representation

    def validate_name(self, value):
        return validate_alphanumeric_and_symbols(value)


class SubCategoryOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order = serializers.IntegerField()