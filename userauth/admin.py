from django.contrib import admin
from .models import Profile

# Register your models here.
class ProflieAdmin(admin.ModelAdmin):
    list_display=['user','first_name','image']

#register
admin.site.register(Profile,ProflieAdmin)