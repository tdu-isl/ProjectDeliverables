from django.urls import path
from django.urls.resolvers import URLPattern
from django.views.generic.detail import DetailView

from . import views

app_name = 'post'

urlpatterns = [
    # path('post_create/', views.post_create, name='post_create'),
    path('', views.show_top, name='top'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='delete'),
    path('post/<int:pk>/', views.show_detail, name='detail'),
    path('post/<int:pk>/like', views.plus_post_like, name='like'),
    path('reply/<int:pk>/', views.create_reply, name='create_reply'),
    path('home/', views.IndexView.as_view(), name='home')
]
