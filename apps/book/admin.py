from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user_name', 'will_come', 'time_stamp',
                    'start_time', 'end_time', 'amount_guest', 'get_tables']


admin.site.register(Book, BookAdmin)
