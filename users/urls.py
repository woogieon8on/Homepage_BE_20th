from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import views, email_auth

app_name = "users"

urlpatterns = [
    path("signup/", views.SignUpView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('activate/<str:uid>/<str:token>',
         email_auth.UserActivateView.as_view(), name='activate'),
]