from .models import Table
from apps.table.models import Floor
from django.db.models import Q

from rest_framework import serializers

def check_dublicate_table(floor_id,number_table,):

    try:
        floor = Floor.objects.get(id=floor_id)
        print("floor: ",floor)
    except Floor.DoesNotExist:
        raise serializers.ValidationError({"floor": "Floor does not exist"})

    # Проверяем наличие столика с данным номером на указанном этаже
    table_exists = Table.objects.filter(floor=floor, number_table=number_table)
    if table_exists.exists():
        raise serializers.ValidationError({"duplicate": "Number Table exists on this floor"})


