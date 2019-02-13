from django.contrib import admin
from .models import PTTPost,PTTLink

# Register your models here.
class PTTadmin(admin.ModelAdmin):
    list_display = ('id','title','date','author','push')
    search_fields = ('title',)
    ordering = ('id','date')
class Linkadmin(admin.ModelAdmin):
    list_display = ('id','link','date')
    ordering =('id','date')

admin.site.register(PTTPost,PTTadmin)
admin.site.register(PTTLink,Linkadmin)

