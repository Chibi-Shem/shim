from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """A custom user model"""
    image = models.ImageField(upload_to = 'papaya/images')
    
    def __str__(self):
        return self.username
