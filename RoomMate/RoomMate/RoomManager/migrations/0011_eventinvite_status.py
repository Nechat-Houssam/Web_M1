# Generated by Django 4.1.7 on 2023-06-21 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoomManager', '0010_eventrequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventinvite',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]