from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (BlogListView, BlogOwnedView,
                    BlogCreateView, BlogEditView,
                    BlogDeleteView, BlogView)


app_name = 'blogs'
urlpatterns = [
    path('',
        BlogListView.as_view(), name='listing'),
    path('blogs',
        BlogOwnedView.as_view(), name='blogs'),
    path('blogs/create',
        BlogCreateView.as_view(), name='blogs_create'),
    path('blogs/<int:blog_id>',
        BlogView.as_view(), name='blogs_view'),
    path('blogs/edit/<int:blog_id>',
        BlogEditView.as_view(), name='blogs_edit'),
    path('blogs/delete/<int:blog_id>',
        BlogDeleteView.as_view(), name='blogs_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)