from rest_framework import generics, response, views
from rest_framework.generics import get_object_or_404
from .models import Book
from .serializers import BookSerializers
from .services import check_overlapping_bookings_update, check_overlapping_bookings
from .tasks import my_task
from django.core.cache import cache
from .book_cache import get_cache_key, get_object_from_cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from datetime import time
from django.http import HttpResponse, Http404

import pandas as pd
import os
from django.db.models import Q
from django.views import View
from django.http import JsonResponse
from .utils import validate_params
from .filters import build_filters
from apps.table.models import Table
from datetime import datetime


CACHE_TIME = 60 * 5
FILE_PATH = 'booking.csv'



def get_current_month():
    return datetime.now().strftime('%Y-%m')

def write_booking_to_file(booking_data):
    # Добавляем текущую дату к данным
    booking_data['date'] = datetime.now().strftime('%Y-%m-%d')
    new_data = pd.DataFrame([booking_data])

    if os.path.exists(FILE_PATH):
        existing_data = pd.read_csv(FILE_PATH)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(FILE_PATH, index=False)

class DownloadBookingFileView(View):
    def get(self, request, *args, **kwargs):
        if os.path.exists(FILE_PATH):
            data = pd.read_csv(FILE_PATH)
            current_month = get_current_month()
            data['date'] = pd.to_datetime(data['date'])
            filtered_data = data[data['date'].dt.strftime('%Y-%m') == current_month]
            filtered_file_path = 'filtered_bookings.csv'
            filtered_data.to_csv(filtered_file_path, index=False)
            with open(filtered_file_path, 'rb') as file:
                response = HttpResponse(file.read(),
                                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(filtered_file_path)}'
                return response
        else:
            raise Http404("File does not exist")

class BookListApiView(generics.ListAPIView):
    serializer_class = BookSerializers
    queryset = Book.objects.all()

    def get_queryset(self):
        queryset = self.queryset.all()

        params, error_response = validate_params(self.request)
        if error_response:
            self.error_response = error_response
            return queryset.none()

        filters = build_filters(params)

        if params['floor_param'] is not None:
            tables = Table.objects.filter(floor_id=params['floor_param'])
            table_ids = tables.values_list('id', flat=True)
            if table_ids:
                queryset = queryset.filter(filters & Q(tables__id__in=table_ids))
            else:
                return queryset.none()
        elif params['table_param'] == 1:
            queryset = queryset.filter(filters & Q(tables__isnull=True))
        elif params['table_param'] == 0:
            queryset = queryset.filter(filters & Q(tables__isnull=False))

        return queryset.filter(filters)

    def list(self, request, *args, **kwargs):
        self.error_response = None
        queryset = self.get_queryset()
        res = my_task.delay("Celery work ...")
        print(res)
        if self.error_response:
            return self.error_response
        serializer = self.serializer_class(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class BookCreateApiView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

    def perform_create(self, serializer):
        new_booking = serializer.validated_data
        new_start_time = new_booking['start_time']
        new_end_time = new_booking['end_time']
        new_table = new_booking.get('tables', [])
        new_date = new_booking['will_come']
        # Проверка на пересечение временных интервалов
        check_overlapping_bookings(new_date, new_start_time, new_end_time, new_table, )
        book_instance = serializer.save()

        booking_data = {
            'id': book_instance.id,
            'user_name': book_instance.user_name,
            'start_time': book_instance.start_time,
            'end_time': book_instance.end_time,
            'will_come': book_instance.will_come,
            'phone_number': book_instance.phone_number,
            'is_come': book_instance.is_come,
            'amount_guest': book_instance.amount_guest,
        }
        ##print(booking_data['start_time'],booking_data['end_time'])
        write_booking_to_file(booking_data)

        cache_key = 'book_ids'
        cached_ids = cache.get(cache_key, [])
        cached_ids.append(book_instance.pk)
        cache.set(cache_key, cached_ids, timeout=CACHE_TIME)
        print(f"Добавлен обьект в кеш: ", cached_ids)


class BookDetailApiView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers


class BookUpdateApiView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

    def perform_update(self, serializer):
        instance = self.get_object()
        new_booking = serializer.validated_data

        new_start_time = new_booking.get('start_time', instance.start_time)
        new_end_time = new_booking.get('end_time', instance.end_time)
        new_date = new_booking.get('will_come', instance.will_come)
        new_phone_number = new_booking.get('phone_number', instance.phone_number)
        new_amount_guest = new_booking.get('amount_guest', instance.amount_guest)
        new_comment = new_booking.get('comment', instance.comment)
        new_table = new_booking.get('tables', instance.tables.all())

        if 'start_time' in new_booking or 'end_time' in new_booking or 'will_come' in new_booking:
            check_overlapping_bookings_update(new_date, new_start_time, new_table, new_end_time, instance.id)
        serializer.save(
            start_time=new_start_time,
            end_time=new_end_time,
            will_come=new_date,
            phone_number=new_phone_number,
            amount_guest=new_amount_guest,
            comment=new_comment
        )


class BookDeleteApiView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers


class AvailableTimesApiView(APIView):
    def post(self, request, *args, **kwargs):
        date_str = request.data.get('date')
        if not date_str:
            return Response({'error': 'Параметр даты обязателен'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            requested_date = parse_date(date_str)
            if not requested_date:
                raise ValueError()
        except ValueError:
            return Response({'error': 'Неверный формат даты'}, status=status.HTTP_400_BAD_REQUEST)

        opening_time = time(10, 0)
        closing_time = time(2, 0)  # Closing time should be 02:00 to cover full day schedule

        bookings = Book.objects.filter(will_come=requested_date).order_by('start_time')

        available_times = []
        occupied_times = []
        current_time = opening_time
        print(bookings)
        for booking in bookings:
            if current_time < booking.start_time:
                available_times.append({
                    'start_time': current_time.strftime("%H:%M"),
                    'end_time': booking.start_time.strftime("%H:%M")
                })
            occupied_times.append({
                'start_time': booking.start_time.strftime("%H:%M"),
                'end_time': booking.end_time.strftime("%H:%M")
            })
            current_time = booking.end_time

        if current_time < closing_time:
            available_times.append({
                'start_time': current_time.strftime("%H:%M"),
                'end_time': closing_time.strftime("%H:%M")
            })

        return Response({
            'date': requested_date.strftime("%Y-%m-%d"),
            'available_times': available_times,
            'occupied_times': occupied_times
        }, status=status.HTTP_200_OK)
    