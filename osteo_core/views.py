from django.http import JsonResponse
from .models import Appointment
from datetime import timedelta

def appointment_api(request):
    appointments = Appointment.objects.filter(status='Confirmed')

    events = []
    for appt in appointments:
        events.append({
            'title': f"{appt.horse.name} ({appt.horse.owner.first_name})",
            'start': appt.date_and_time.isoformat(),
            'end': (appt.date_and_time + timedelta(hours=1)).isoformat(),
            'color': '#28a745'
        })
    return JsonResponse(events, safe=False)