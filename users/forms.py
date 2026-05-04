from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    is_practitoner = forms.BooleanField(
        required=False,
        label="Are you a practitioner?",
        help_text="Check this box if you provide services and manage clients/horses."
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('is_practitioner'):
            user.is_staff = True
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError("A user with that email already exists.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            return first_name.strip().title()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            return last_name.strip().title()
        return last_name