from django.db import models
from django.conf import settings
from django.db.models import JSONField

class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Horse(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    owner = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='horses')

    def __str__(self):
        return f"{self.name} (Owner: {self.owner.first_name} {self.owner.last_name})"
    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending Request'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='appointments')
    date_and_time =  models.DateTimeField()
    reason_for_visit = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    is_completed = models.BooleanField(default=False)
    #client_paid = models.BooleanField(default=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.horse.name} - {self.date_and_time.strftime('%b %d, %Y at %I:%M %p')}"

class Assessment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='assessment')
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='assessments')
    date_performed = models.DateTimeField(auto_now_add=True)
    assessment_data = models.JSONField(default=dict)
    general_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Assessment: {self.horse.name} ({self.date_performed.strftime('%Y-%m-%d')})"