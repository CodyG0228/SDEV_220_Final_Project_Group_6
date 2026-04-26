from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from osteo_core import views as osteo_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
    path('api/appointments/', osteo_views.appointment_api, name='appointment_api'),
    path('', osteo_views.dashboard_view, name='home'),
    path('horse/<int:pk>/', osteo_views.horse_detail, name='horse_detail'),
    path('appointment/<int:pk>/approve/', osteo_views.approve_appointment, name='approve_appointment'),
    path('appointment/<int:pk>/assessment/new/', osteo_views.create_assessment, name='create_assessment'),
    path('request-appointment/', osteo_views.request_appointment, name='request_appointment'),
    path('request-success/', TemplateView.as_view(template_name='request_success.html'), name='request_success'),
    path('add-horse/', osteo_views.add_horse, name='add_horse'),
    path('profile/', osteo_views.edit_profile, name='edit_profile'),
    path('my-horses/', osteo_views.my_horses, name='my_horses'),
    path('horse/<int:pk>/edit/', osteo_views.edit_horse, name='edit_horse'),
    path('assessment/<int:pk>/edit/', osteo_views.edit_assessment, name='edit_assessment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)