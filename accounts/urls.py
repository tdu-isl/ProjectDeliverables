from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/<str:username>/', views.user_profile, name='profile')
]