
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
    path('appointment/<int:pk>/approve/', osteo_views.approve_appointment, name='approve_appointment'),
    path('request-appointment/', osteo_views.request_appointment, name='request_appointment'),
    path('request-success/', TemplateView.as_view(template_name='request_success.html'), name='request_success'),
    path('', osteo_views.dashboard_view, name='home'),
]
