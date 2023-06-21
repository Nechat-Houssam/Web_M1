from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Room, Event
from datetime import datetime, timedelta

class RoomModelTest(TestCase):
    def test_room_creation(self):
        room = Room.objects.create(
            name='Salle de réunion',
            capacity=10,
            wing='P',
            floor=1,
            number=101
        )

        self.assertEqual(room.name, 'Salle de réunion')
        self.assertEqual(room.capacity, 10)
        self.assertEqual(room.wing, 'P')
        self.assertEqual(room.floor, 1)
        self.assertEqual(room.number, 101)



class DeleteEventTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='john', password='password')
        self.room = Room.objects.create(
            name='Salle de réunion',
            capacity=10,
            wing='P',
            floor=1,
            number=101
        )
        self.event = Event.objects.create(
            creator=self.user,
            date=datetime.now().date(),
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=2),
            room=self.room
        )

    def test_delete_event(self):
        login = self.client.login(username='john', password='password')
        self.assertTrue(login)

        response = self.client.post(reverse('delete_event'), {
            'start_time': self.event.start_time,
        })

        self.assertEqual(response.status_code, 200)

        # Vérifiez si l'événement a été supprimé de la base de données
        event_exists = Event.objects.filter(pk=self.event.pk).exists()
        self.assertFalse(event_exists)


