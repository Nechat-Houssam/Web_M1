from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    ROLES = [
        ('N', 'normal'),
        ('M', 'moderator'),
        ('A', 'administrator'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=1, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

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
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_creator", default=None)
    invited = models.ManyToManyField(User, related_name="event_invited", default=None)
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

class EventInvite(models.Model):
    from_event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="invite_from_event", null=True)
    to_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invite_to_profile", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite from {self.from_event} to {self.to_profile}"
    
class EventRequest(models.Model):
    from_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_from_profile", null=True)
    to_event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="request_to_event", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.from_profile} to {self.to_event}"