from django import forms
from .models import Appointment

class AppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['horse', 'date_and_time', 'reason_for_visit', 'notes']

        widgets = {
            'date_and_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
        }