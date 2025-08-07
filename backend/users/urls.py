from django.urls import path
from .views import ChangePasswordView, RegisterView, LoginView, LogoutView, UserMeView, VerifyEmailView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me",  UserMeView.as_view(), name="user-me"),
    path("change_password/", ChangePasswordView.as_view() ,name="chane_password"),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
]