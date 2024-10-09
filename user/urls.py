from django.urls import path
from .views import signIn, signOut, signUp, add_info

urlpatterns = [
    path("signup/", signUp, name="register"),
    path("signin/", signIn, name="login"),
    path("signOut/", signOut, name="logOut"),
    path("add_info/", add_info, name="add_info"),
]
