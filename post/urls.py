from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

app_name = 'post'

urlpatterns = [
    # path('post_create/', views.post_create, name='post_create'),
    path('', views.show_top, name='top'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('home/', views.IndexView.as_view(), name='home')
]