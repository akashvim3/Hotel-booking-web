from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('guest', 'Guest'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    is_hotel_owner = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    # ...add more fields as needed...
