from django.urls import path
from .views.tickets_views import FreshmanViewSet, GeneralTicketListViewSet
from .views.application_views import ApplicationViewSet

app_name = 'kahlua_admin'

urlpatterns = [
    path('tickets/freshman_tickets/', FreshmanViewSet.as_view({'get':'list'}), name='freshman_list'),
    path('tickets/general_tickets/', GeneralTicketListViewSet.as_view({'get':'list'}), name='general_list'),
    path('application/apply_forms/', ApplicationViewSet.as_view({'get':'list'}), name='applyforms_list'),    
]