from django import forms
from django.forms import ModelForm
from .models import Blog


class BlogForm(ModelForm):
    """Blog form for users"""
    class Meta:
        model = Blog
        fields = ['image', 'title', 'author', 'category', 'content']

    image = forms.ImageField(widget=forms.FileInput, required=False,
                            label="Image:")
