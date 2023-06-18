from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    WINGS = [
        ('P', 'Paris'),
        ('B', 'Boulogne'),
        ('A', 'Auteuil'),
    ]
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    wing = models.CharField(max_length=1, choices=WINGS)
    floor = models.IntegerField()
    number = models.IntegerField()

    def __str__(self):
        return self.name
    
class Event(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)