from rest_framework import serializers
from .models import Book
from datetime import datetime, time, timedelta
from django.db.models import Q


def check_overlapping_bookings(new_date, new_start_time, new_end_time, new_table=None, ):
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    previous_day = current_date - timedelta(days=1)
    not_allowed_end_time = time(4, 0, 0)

    if new_date < previous_day or (new_date == previous_day and current_date == previous_day and current_time >= not_allowed_end_time):
        raise serializers.ValidationError({"date": "Дата бронирования уже прошла."})

    allowed_start_time = time(10, 0, 0)
    if not (allowed_start_time <= new_start_time or new_start_time <= not_allowed_end_time):
        raise serializers.ValidationError(
            {"start_time": "Время начала бронирования должно быть между 10:00 и 4:00 следующего дня."})

    if not (new_end_time <= not_allowed_end_time or new_end_time >= allowed_start_time):
        raise serializers.ValidationError(
            {"end_time": "Время окончания бронирования должно быть между 10:00 и 4:00 следующего дня."})

    if new_table is not None:
        
        if new_end_time < new_start_time:
            overlapping_bookings = Book.objects.filter(
                Q(tables__in=new_table) &
                Q(will_come=new_date) &
                (Q(start_time__lt=new_end_time) | Q(end_time__gt=new_start_time))
            )
        else:
            overlapping_bookings = Book.objects.filter(
                Q(tables__in=new_table) &
                Q(will_come=new_date) &
                Q(start_time__lt=new_end_time) & Q(end_time__gt=new_start_time)
            )
        if overlapping_bookings.exists():
            raise serializers.ValidationError({"occupated": "В это время уже есть бронирование."})


def check_overlapping_bookings_update(new_date, new_start_time, new_table, new_end_time, instance_id=None):
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    previous_day = current_date - timedelta(days=1)
    not_allowed_end_time = time(4, 0, 0)

    if new_date < previous_day or (new_date == previous_day and current_date == previous_day and current_time >= not_allowed_end_time):
        raise serializers.ValidationError({"date": "Дата бронирования уже прошла."})

    allowed_start_time = time(10, 0, 0)
    if not (allowed_start_time <= new_start_time or new_start_time <= not_allowed_end_time):
        raise serializers.ValidationError(
            {"start_time": "Время начала бронирования должно быть между 10:00 и 4:00 следующего дня."})

    if not (new_end_time <= not_allowed_end_time or new_end_time >= allowed_start_time):
        raise serializers.ValidationError(
            {"end_time": "Время окончания бронирования должно быть между 10:00 и 4:00 следующего дня."})

    # if new_end_time < new_start_time:
    #     end_time_query = Q(start_time__lt=new_end_time) | Q(end_time__gt=new_start_time)
    # else:
    #     end_time_query = Q(start_time__lt=new_end_time, end_time__gt=new_start_time)

    if new_table is not None:
            if new_end_time < new_start_time:
                overlapping_bookings = Book.objects.filter(
                    Q(tables__in=new_table) &
                    Q(will_come=new_date) &
                    (Q(start_time__lt=new_end_time) | Q(end_time__gt=new_start_time))
                )
            else:
                overlapping_bookings = Book.objects.filter(
                    Q(tables__in=new_table) &
                    Q(will_come=new_date) &
                    Q(start_time__lt=new_end_time) & Q(end_time__gt=new_start_time)
                )
            if instance_id:
                overlapping_bookings = overlapping_bookings.exclude(id=instance_id)

            if overlapping_bookings.exists():
                raise serializers.ValidationError({"occupated": "В это время уже есть бронирование."})
