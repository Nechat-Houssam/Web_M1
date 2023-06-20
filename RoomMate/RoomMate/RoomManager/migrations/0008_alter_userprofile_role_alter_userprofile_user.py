# Generated by Django 4.2.1 on 2023-06-20 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RoomManager', '0007_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('N', 'normal'), ('M', 'moderator'), ('A', 'administrator')], max_length=1),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]