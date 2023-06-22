from django.contrib import admin
from .models import UserProfile, Room, Event, EventRequest, Note

admin.site.register(Room)
admin.site.register(Event)
admin.site.register(UserProfile)
admin.site.register(EventRequest)
admin.site.register(Note)