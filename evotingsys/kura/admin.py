from django.contrib import admin
from .models import Candidate,Position
# Register your models here.
class PositionAdmin(admin.ModelAdmin):
    fields = ['id', 'name']

admin.site.register(Position)
admin.site.register(Candidate)