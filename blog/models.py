from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    #Adding a function that will allow us to change the Published date from Blank to Current Date
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    #We are going to add a string method to display the name of something in the terminal if we need it

    def __str__(self):
        return self.title

