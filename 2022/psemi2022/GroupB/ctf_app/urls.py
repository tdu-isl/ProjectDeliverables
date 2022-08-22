from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='index'),
    path('signup', views.UserCreateView.as_view(), name='signup'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('new', views.QuestionCreateView.as_view(), name='new'),
    path('<int:pk>', views.QuestionShowView.as_view(), name='question')
]
