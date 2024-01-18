from django.urls import path
from .views import ApplyCreateView, ApplyCompleteView

urlpatterns = [
    path('apply/', ApplyCreateView.as_view(), name='apply'),
    path('apply_complete/', ApplyCompleteView.as_view(), name='apply_complete')
]