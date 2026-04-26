from django.contrib import admin
from .models import Client, Horse, Appointment, Assessment, Profile

admin.site.register(Client)
admin.site.register(Horse)
admin.site.register(Appointment)
admin.site.register(Assessment)
admin.site.register(Profile)