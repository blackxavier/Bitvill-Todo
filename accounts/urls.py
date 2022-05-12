from django.urls import path
from accounts.views import (
    registration_view,
    UserProfileView,
    ObtainAuthTokenView,
    ChangePasswordView,
    user_logout,
    user_logout
)

app_name = "accounts"

urlpatterns = [
    path("register/", registration_view, name="register"),
    path("login/", ObtainAuthTokenView.as_view(), name="login"),
    path("logout/", user_logout, name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("me/", UserProfileView, name="change-password"),
]
