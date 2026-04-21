from django.http import JsonResponse
from .models import Appointment
from datetime import timedelta
from .forms import AppointmentRequestForm

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

def request_appointment(request):
    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AppointmentRequestForm()
    
    return render(request, 'request_appointment.html', {'form': form})