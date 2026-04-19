
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from osteo_core import views as osteo_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
    path('api/appointments/', osteo_views.appointment_api, name='appointment_api'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
