from django.urls import path
from .views import ChangePasswordView, RegisterView, LoginView, LogoutView, UserMeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me",  UserMeView.as_view(), name="user-me"),
    path("change_password/", ChangePasswordView.as_view() ,name="chane_password")
]