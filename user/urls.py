from django.urls import path
from .views import signUp, signIn, signOut

urlpatterns = [
    path("signin/", signIn),
    path("signup/", signUp),
    path("signout/", signOut),
]
