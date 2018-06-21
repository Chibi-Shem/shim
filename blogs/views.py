from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BlogForm
from .models import Blog


class BlogOwnedView(LoginRequiredMixin, TemplateView):
    """Displays the user's blogs page"""
    template_name = 'blogs.html'
    
    def get(self, *args, **kwargs):
        return render(self.request, self.template_name,
                {'blogs':Blog.objects.filter(author=self.request.user)})


class BlogCreateView(LoginRequiredMixin, TemplateView):
    """Displays the create blogs page"""
    template_name = 'blogs_create.html'
    
    def get(self, *args, **kwargs):
        form = BlogForm(initial={'author':self.request.user})
        return render(self.request, self.template_name,
                     {'form':form})

    def post(self, *args, **kwargs):
        form = BlogForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('blogs:blogs'))
        return render(self.request, self.template_name,
                     {'form':form})


class BlogEditView(LoginRequiredMixin, TemplateView):
    """Displays the blog's edit page"""
    template_name = 'blogs_create.html'
    
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
            return redirect(reverse('blogs:blogs_view', args=(blog_id,)))
        return render(self.request, self.template_name,
                    {'form':form, 'blog_image':blog.image})


class BlogDeleteView(LoginRequiredMixin, TemplateView):
    """Deletes a blog """
    
    def get(self, *args, **kwargs):
        blog_id = kwargs.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id, author=self.request.user)
        blog.delete()
        return redirect(reverse('blogs:blogs'))


class BlogView(TemplateView):
    """Displays the blog's detail page"""
    template_name = 'blogs_view.html'

    def get(self, *args, **kwargs):
        blog_id = kwargs.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id)
        return render(self.request, self.template_name,
                     {'blog':blog})


class BlogListView(TemplateView):
    """Displays the list of all blogs"""
    template_name = "listing.html"
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
