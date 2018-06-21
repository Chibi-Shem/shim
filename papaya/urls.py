from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import BlogListView, ProfileCreateView, ProfileEditView
from .views import ProfileChangepassView, ProfileLoginView, ProfileLogoutView
from .views import ProfileView, BlogOwnedView, BlogCreateView, BlogEditView
from .views import BlogDeleteView, BlogView

app_name = 'papaya'
urlpatterns = [
    path('',
        BlogListView.as_view(), name='listing'),
    path('profile/<int:profile_id>',
        ProfileView.as_view(), name='profile'),
    path('profile/create',
        ProfileCreateView.as_view(), name='profile_create'),
    path('profile/edit',
        ProfileEditView.as_view(), name='profile_edit'),
    path('profile/changepass',
        ProfileChangepassView.as_view(), name='profile_changepass'),
    path('profile/login',
        ProfileLoginView.as_view(), name='profile_login'),
    path('profile/logout',
        ProfileLogoutView.as_view(), name='profile_logout'),
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