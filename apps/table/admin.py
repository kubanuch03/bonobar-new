from django.contrib import admin

from .models import Table


class TableAdmin(admin.ModelAdmin):
    list_display = ['id', 'number_table', 'occupated', 'floor', 'display_books']

    def display_books(self, obj):
        return ", ".join([book.title for book in obj.books.all()])
    display_books.short_description = 'Books'


admin.site.register(Table, TableAdmin)
