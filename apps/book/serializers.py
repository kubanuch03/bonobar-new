from rest_framework import serializers

from .models import Book
from apps.table.models import Table


class TableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id', 'number_table')


class BookSerializers(serializers.ModelSerializer):
    table_set = serializers.SerializerMethodField()
    tables = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all(), many=True, required=False)

    def get_table_set(self, obj):
        tables = obj.tables.all()
        table_set = [TableListSerializer(table).data for table in tables]
        return table_set

    def create(self, validated_data):
        tables_data = validated_data.pop('tables', [])
        book = Book.objects.create(**validated_data)
        book.tables.set(tables_data)
        return book

    def update(self, instance, validated_data):
        tables_data = validated_data.pop('tables', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if tables_data is not None:
            instance.tables.set(tables_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if "tables" in representation:
            del representation["tables"]
        return representation

    class Meta:
        model = Book
        fields = ['id', 'user_name', 'phone_number', 'will_come', 'time_stamp', 'start_time', 'end_time',
                  'amount_guest', 'tables', 'comment', 'is_come', 'created_at', 'table_set']

        extra_kwargs = {
                'user_name': {'required': False},
                'phone_number': {'required': False},
                'comment': {'required': False},
            }
