from django import forms
from .models import Appointment, Horse, Profile, Client
from django.contrib.auth import get_user_model

User = get_user_model()

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
        self.fields['practitioner'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}".strip() or obj.username

class HorseForm(forms.ModelForm):
    class Meta:
        model = Horse
        fields = ['name', 'breed', 'age']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'phone_number', 'location']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(555) 555-5555'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State'}),
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['phone_number', 'address']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(555) 555-5555'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State'}),
        }