from django.urls import path
from .views import RegisterView, profile

app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
]
