from django.urls import path
from .views import test_api, register, me, login, logout, google_login, extension_login
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', test_api),
    path('register/', register),
    path("login/", login, name="login"),
    path("extension-login/", extension_login, name="extension-login"),  # NEW
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("me/", me),
    path("logout/", logout),
    path("auth/google/", google_login),
]