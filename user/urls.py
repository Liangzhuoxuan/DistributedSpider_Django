from django.urls import path
from .views import *

urlpatterns = [
    path('login.html', loginView, name="login"),
    path('register.html', registerView, name="register"),
]