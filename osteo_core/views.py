import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import timedelta
from .models import Appointment, Horse, Assessment, Profile
from .forms import AppointmentRequestForm, HorseForm, ProfileForm

def dashboard_view(request):
    if request.user.is_staff:
        pending_requests = Appointment.objects.filter(status='Pending', practitioner=request.user).order_by('date_and_time')
        return render(request, 'home.html', {'pending_requests': pending_requests})
    else:
        client_profile = getattr(request.user, 'client', None)
        
        if client_profile:
            client_appointments = Appointment.objects.filter(horse__owner=client_profile).order_by('-date_and_time')
        else:
            client_appointments = []
            
        return render(request, 'home.html', {'client_appointments': client_appointments})

def approve_appointment(request, pk):
    if request.method == 'POST':
        appt = get_object_or_404(Appointment, pk=pk)
        appt.status = 'Confirmed'
        appt.save()
    return redirect('home')

def appointment_api(request):
    appointments = Appointment.objects.filter(status='Confirmed', practitioner=request.user)
    
    events = []
    for appt in appointments:
        events.append({
            'title': f"{appt.horse.name} ({appt.horse.owner.first_name})",
            'start': appt.date_and_time.isoformat(), 
            'end': (appt.date_and_time + timedelta(hours=1)).isoformat(), 
            'color': '#28a745',
            'url': f'/horse/{appt.horse.id}/',
        })
    return JsonResponse(events, safe=False)

def request_appointment(request):
    current_client = getattr(request.user, 'client', None)
    if not current_client:
        return redirect('edit_profile')
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

def create_assessment(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, pk=pk)

    if hasattr(appointment, 'assessment'):
        return redirect('horse_detail', pk=appointment.horse.pk)

    if request.method == 'POST':
        raw_json_string = request.POST.get('assessment_data', '{}')
        
        try:
            assessment_dict = json.loads(raw_json_string)
        except json.JSONDecodeError:
            assessment_dict = {}
        notes = request.POST.get('general_notes', '')
        Assessment.objects.create(
            appointment=appointment,
            horse=appointment.horse,
            assessment_data=assessment_dict,
            general_notes=notes
        )
        
        return redirect('horse_detail', pk=appointment.horse.pk)

    return render(request, 'assessment_form.html', {'appointment': appointment})

def add_horse(request):
    current_client = getattr(request.user, 'client', None)
    if not current_client:
        return redirect('edit_profile')

    if request.method == 'POST':
        form = HorseForm(request.POST)
        if form.is_valid():
            new_horse = form.save(commit=False)
            new_horse.owner = current_client
            new_horse.save()
            return redirect('home')
    else:
        form = HorseForm()

    return render(request, 'add_horse.html', {'form': form})

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})

def my_horses(request):
    current_client = getattr(request.user, 'client', None)
    if not current_client:
        return redirect('edit_profile')
        
    horses = Horse.objects.filter(owner=current_client)
    return render(request, 'my_horses.html', {'horses': horses})

def edit_horse(request, pk):
    current_client = getattr(request.user, 'client', None)
    if not current_client:
        return redirect('home')

    horse = get_object_or_404(Horse, pk=pk)

    if horse.owner != current_client:
        return redirect('home')

    if request.method == 'POST':
        form = HorseForm(request.POST, instance=horse)
        if form.is_valid():
            form.save()
            return redirect('my_horses')
    else:
        form = HorseForm(instance=horse)

    return render(request, 'edit_horse.html', {'form': form, 'horse': horse})

def edit_assessment(request, pk):
    if not request.user.is_staff:
        return redirect('home')
        
    assessment = get_object_or_404(Assessment, pk=pk)
    appointment = assessment.appointment

    if request.method == 'POST':
        raw_json_string = request.POST.get('assessment_data', '{}')
        try:
            assessment_dict = json.loads(raw_json_string)
        except json.JSONDecodeError:
            assessment_dict = assessment.assessment_data # If invalid, revert to old data
            
        assessment.assessment_data = assessment_dict
        assessment.general_notes = request.POST.get('general_notes', assessment.general_notes)
        assessment.save()
        
        return redirect('horse_detail', pk=appointment.horse.pk)
    return render(request, 'assessment_form.html', {'appointment': appointment, 'assessment': assessment})

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing_page.html')