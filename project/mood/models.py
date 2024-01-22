from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Mood(models.Model):
    rating = models.IntegerField()
    created_at = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True, blank=True)

class Rant(models.Model):
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
