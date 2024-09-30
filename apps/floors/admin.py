from django.contrib import admin
from .models import Floor

class FloorAdmin(admin.ModelAdmin):
    list_display = ['id','title']

admin.site.register(Floor,FloorAdmin)