from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegistrationForm, UserEditForm
from .forms import UserChangepassForm, BlogForm, UserLoginForm
from .models import Blog, User


class ProfileCreateView(TemplateView):
    """Displays the user's registration page"""
    template_name = "papaya/profile_create.html"

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
            return redirect(reverse('papaya:listing'))
        return render(self.request, self.template_name, {'form':form})


class ProfileEditView(LoginRequiredMixin, TemplateView):
    """Displays the user's edit page"""
    template_name = "papaya/profile_edit.html"
    
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
            return redirect(reverse('papaya:profile',
                                args=(user.id,)))
        return render(self.request, self.template_name,
                {'form':form, 'profile_image':user.image})


class ProfileChangepassView(LoginRequiredMixin, TemplateView):
    """Displays the user's edit password page"""
    template_name = "papaya/profile_changepass.html"
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
                return redirect(reverse('papaya:profile',
                            args=(self.request.user.id,)))
            else:
                self.error = 'Invalid password'
        return render(self.request, self.template_name,
                     {'form':form, 'error':self.error})


class ProfileLoginView(TemplateView):
    """Displays the user's login page"""
    template_name = "papaya/profile_login.html"
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
                return redirect(reverse('papaya:listing'))
            else:
                self.error = 'Invalid username or password'
        return render(self.request, self.template_name,
                     {'form':form,'error':self.error})


class ProfileLogoutView(TemplateView):
    """Logs out a user"""
    
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect(reverse('papaya:listing'))


class ProfileView(TemplateView):
    """Displays the user's profile page"""
    template_name = 'papaya/profile.html'
    
    def get(self, *args, **kwargs):
        profile_id = kwargs.get('profile_id')
        user = get_object_or_404(User, id=profile_id)
        return render(self.request, self.template_name, {'profile':user})


class BlogOwnedView(LoginRequiredMixin, TemplateView):
    """Displays the user's blogs page"""
    template_name = 'papaya/blogs.html'
    
    def get(self, *args, **kwargs):
        return render(self.request, self.template_name,
                {'blogs':Blog.objects.filter(author=self.request.user)})


class BlogCreateView(LoginRequiredMixin, TemplateView):
    """Displays the create blogs page"""
    template_name = 'papaya/blogs_create.html'
    
    def get(self, *args, **kwargs):
        form = BlogForm(initial={'author':self.request.user})
        return render(self.request, self.template_name,
                     {'form':form})

    def post(self, *args, **kwargs):
        form = BlogForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('papaya:blogs'))
        return render(self.request, self.template_name,
                     {'form':form})


class BlogEditView(LoginRequiredMixin, TemplateView):
    """Displays the blog's edit page"""
    template_name = 'papaya/blogs_create.html'
    
    def get(self, *args, **kwargs):
        blog_id = kwargs.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id, author=self.request.user)
        form = BlogForm(instance=blog)
        return render(self.request, self.template_name,
                    {'form':form, 'blog_image':blog.image})

    def post(self, *args, **kwargs):
        blog_id = kwargs.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id, author=self.request.user)
        form = BlogForm(self.request.POST, self.request.FILES, instance=blog)
        if form.is_valid():
            if not self.request.FILES:
                form.cleaned_data['image'] = blog.image
            form.save()
            return redirect(reverse('papaya:blogs_view', args=(blog_id,)))
        return render(self.request, self.template_name,
                    {'form':form, 'blog_image':blog.image})


class BlogDeleteView(LoginRequiredMixin, TemplateView):
    """Deletes a blog """
    
    def get(self, *args, **kwargs):
        blog_id = kwargs.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id, author=self.request.user)
        blog.delete()
        return redirect(reverse('papaya:blogs'))


class BlogView(TemplateView):
    """Displays the blog's detail page"""
    template_name = 'papaya/blogs_view.html'

    def get(self, *args, **kwargs):
        blog_id = kwargs.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id)
        return render(self.request, self.template_name,
                     {'blog':blog})


class BlogListView(TemplateView):
    """Displays the list of all blogs"""
    template_name = "papaya/listing.html"
    msg = ''

    def get(self, *args, **kwargs):
        blogs = Blog.objects.all()
        return render(self.request, self.template_name,
                {'blogs':blogs, 'msg':self.msg})

    def post(self, *args, **kwargs):
        searchword = self.request.POST['search']
        blogs = Blog.objects.filter(title__icontains=searchword)
        if not blogs:
            self.msg = 'No results found!'
        return render(self.request, self.template_name,
                {'blogs':blogs, 'msg':self.msg})
