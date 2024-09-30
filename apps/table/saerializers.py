from rest_framework import serializers
from .models import Table
from apps.floors.serializers import FloorSerializer
from apps.book.serializers import BookSerializers
from .services import check_dublicate_table

class TableListSerializer(serializers.ModelSerializer):
    floor = FloorSerializer()
    books = BookSerializers(many=True)

    class Meta:
        model = Table
        fields = ['id', 'number_table', 'occupated', 'books', 'floor']

    def to_representation(self, instance):
        data_table = super().to_representation(instance)
        data_table['floor'] = FloorSerializer(instance.floor).data
        data_table['books'] = BookSerializers(instance.books.all(), many=True).data
        return data_table


class TableCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = ['id', 'number_table', 'occupated', 'books', 'floor']

    def validate(self, data):
        floor_id = data.get('floor').id
        print('serializers: ',floor_id)

        number_table = data.get('number_table')
        check_dublicate_table(floor_id, number_table)
        return data
    