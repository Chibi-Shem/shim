from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (ProfileCreateView, ProfileEditView,
                    ProfileChangepassView, ProfileLoginView,
                    ProfileLogoutView, ProfileView)


app_name = 'users'
urlpatterns = [
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
