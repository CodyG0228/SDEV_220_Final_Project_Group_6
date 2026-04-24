from django.contrib import admin
from .models import Client, Horse, Appointment, Assessment

admin.site.register(Client)
admin.site.register(Horse)
admin.site.register(Appointment)
admin.site.register(Assessment)