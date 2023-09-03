
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    CHOICE = (
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
    )
    user_choice = models.CharField(max_length=20, choices=CHOICE, default='Viewer')
