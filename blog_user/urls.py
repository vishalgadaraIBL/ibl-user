from django.urls import path
from .views import UserCreateView, LoginView, test

urlpatterns = [
    path('user_create/',UserCreateView.as_view()),
    path('user_login/', LoginView.as_view()),
    path('test/', test.as_view()),
]