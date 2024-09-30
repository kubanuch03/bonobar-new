from django.contrib import admin
from .models import BanerMain, BanerMiddle, BanerBook, BanerMainTopik


class BanerMainAdmin(admin.ModelAdmin):
    list_display = ['id','title','subtitle',]


class BanerMainTopikAdmin(admin.ModelAdmin):
    list_display = ['id','img']


class BanerMiddleAdmin(admin.ModelAdmin):
    list_display = ['id','title']


class BanerBookAdmin(admin.ModelAdmin):
    list_display = ['id','title']


admin.site.register(BanerMain,BanerMainAdmin)
admin.site.register(BanerMainTopik,BanerMainTopikAdmin)
admin.site.register(BanerMiddle,BanerMiddleAdmin)
admin.site.register(BanerBook,BanerBookAdmin)
