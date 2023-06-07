from django.db import models

# Create your models here.

class Room(models.Model):
    WINGS = [
        ('P', 'Paris'),
        ('B', 'Boulogne'),
        ('A', 'Auteuil'),
    ]
    name = models.CharField(max_length=50)
    capacity = models.IntegerField(max_length=2)
    wing = models.CharField(max_length=1, choices=WINGS)
    floor = models.IntegerField(max_length=1)
    number = models.IntegerField(max_length=2)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)