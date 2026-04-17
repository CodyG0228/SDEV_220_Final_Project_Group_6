from django.db import models

class Client(models.Model):
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