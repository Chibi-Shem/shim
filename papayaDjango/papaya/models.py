from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """A category model"""
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Blog(models.Model):
    """A blog model"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    content = models.TextField()

    def __str__(self):
        return self.title
