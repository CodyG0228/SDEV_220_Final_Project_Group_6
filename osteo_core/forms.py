from django import forms
from .models import Appointment, Horse

class AppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['practitioner', 'horse', 'date_and_time', 'reason_for_visit', 'notes'] 
        widgets = {
            'date_and_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        super(AppointmentRequestForm, self).__init__(*args, **kwargs)

        if client:
            self.fields['horse'].queryset = Horse.objects.filter(owner=client)

class HorseForm(forms.ModelForm):
    class Meta:
        model = Horse
        # Notice we DO NOT include 'owner' here. The user shouldn't pick the owner; we will force it in the view!
        fields = ['name', 'breed', 'age']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }