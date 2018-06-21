from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (UserRegistrationForm, UserEditForm,
                    UserChangepassForm, UserLoginForm)
from .models import User


class ProfileCreateView(TemplateView):
    """Displays the user's registration page"""
    template_name = "profile_create.html"

    def get(self, *args, **kwargs):
        form = UserRegistrationForm()
        return render(self.request, self.template_name, {'form':form})

    def post(self, *args, **kwargs):
        form = UserRegistrationForm(self.request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(self.request,
                                username=username,
                                password=password)
            login(self.request, user)
            return redirect(reverse('blogs:listing'))
        return render(self.request, self.template_name, {'form':form})


class ProfileEditView(LoginRequiredMixin, TemplateView):
    """Displays the user's edit page"""
    template_name = "profile_edit.html"
    
    def get(self, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        form = UserEditForm(instance=user)
        return render(self.request, self.template_name,
                {'form':form, 'profile_image':user.image})

    def post(self, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        form = UserEditForm(self.request.POST, self.request.FILES, instance=user)
        if form.is_valid():
            if not self.request.FILES:
                form.cleaned_data['image'] = user.image
            form.save()
            return redirect(reverse('users:profile',
                                args=(user.id,)))
        return render(self.request, self.template_name,
                {'form':form, 'profile_image':user.image})


class ProfileChangepassView(LoginRequiredMixin, TemplateView):
    """Displays the user's edit password page"""
    template_name = "profile_changepass.html"
    error = ''
    
    def get(self, *args, **kwargs):
        username = self.request.user.username
        user = User.objects.get(username=username)
        form = UserChangepassForm()
        return render(self.request, self.template_name,
                     {'form':form, 'error':self.error})

    def post(self, *args, **kwargs):
        username = self.request.user.username
        form = UserChangepassForm(self.request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(self.request,
                                username=username,
                                password=password)
            if user is not None:
                form.update(username)
                password_new = form.cleaned_data['password_new']
                user = authenticate(self.request,
                                    username=username,
                                    password=password_new)
                login(self.request, user)
                return redirect(reverse('users:profile',
                            args=(self.request.user.id,)))
            else:
                self.error = 'Invalid password'
        return render(self.request, self.template_name,
                     {'form':form, 'error':self.error})


class ProfileLoginView(TemplateView):
    """Displays the user's login page"""
    template_name = "profile_login.html"
    error = ''
    
    def get(self, *args, **kwargs):
        form = UserLoginForm()
        return render(self.request, self.template_name,
                     {'form':form,'error':self.error})

    def post(self, *args, **kwargs):
        form = UserLoginForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(self.request,
                        username=username,
                        password=password)
            if user is not None:
                login(self.request, user)
                return redirect(reverse('blogs:listing'))
            else:
                self.error = 'Invalid username or password'
        return render(self.request, self.template_name,
                     {'form':form,'error':self.error})


class ProfileLogoutView(TemplateView):
    """Logs out a user"""
    
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect(reverse('blogs:listing'))


class ProfileView(TemplateView):
    """Displays the user's profile page"""
    template_name = 'profile.html'
    
    def get(self, *args, **kwargs):
        profile_id = kwargs.get('profile_id')
        user = get_object_or_404(User, id=profile_id)
        return render(self.request, self.template_name, {'profile':user})
