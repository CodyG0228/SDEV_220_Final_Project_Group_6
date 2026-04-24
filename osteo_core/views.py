from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import timedelta
from .models import Appointment, Horse
from .forms import AppointmentRequestForm

def dashboard_view(request):
    pending_requests = Appointment.objects.filter(status='Pending').order_by('date_and_time')
    return render(request, 'home.html', {'pending_requests': pending_requests})

def approve_appointment(request, pk):
    if request.method == 'POST':
        appt = get_object_or_404(Appointment, pk=pk)
        appt.status = 'Confirmed'
        appt.save()
    return redirect('home')

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
    current_client = getattr(request.user, 'client', None)

    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST, client=current_client)
        if form.is_valid():
            form.save()
            return redirect('request_success') 
    else:
        form = AppointmentRequestForm(client=current_client)

    return render(request, 'request_appointment.html', {'form': form})

def horse_detail(request, pk):
    horse = get_object_or_404(Horse, pk=pk)
    appointments = horse.appointments.all().order_by('-date_and_time')
    return render(request, 'horse_detail.html', {'horse': horse, 'appointments': appointments})