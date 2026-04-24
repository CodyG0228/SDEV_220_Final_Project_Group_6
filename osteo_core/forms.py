from django import forms
from .models import Appointment, Horse

class AppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['horse', 'date_and_time', 'reason_for_visit', 'notes']

        widgets = {
            'date_and_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        super(AppointmentRequestForm, self).__init__(*args, **kwargs)

        if client:
            self.fields['horse'].queryset = Horse.objects.filter(owner=client)