from django.urls import path
from .views import signUp, signIn, signOut

urlpatterns = [
    path("signin/", signIn, name="login"),
    path("signup/", signUp, name="register"),
    path("signout/", signOut, name="logout"),
]
