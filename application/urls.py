from django.urls import path
from .views import ApplyCreateView

urlpatterns = [
    path('apply/', ApplyCreateView.as_view(), name='apply'),
]