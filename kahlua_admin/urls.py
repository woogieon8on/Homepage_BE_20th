from django.urls import path
from .views.tickets_views import FreshmanViewSet, GeneralTicketListViewSet

app_name = 'kahlua_admin'

urlpatterns = [
    path('tickets/freshman_tickets/', FreshmanViewSet.as_view({'get':'list'}), name='freshman_list'),
    path('tickets/general_tickets/list/', GeneralTicketListViewSet.as_view({'get':'list'}), name='general_list'),
    # path('tickets/general_tickets/detail/', GeneralTicketDetailViewSet.as_view({'get':'get'}), name='general_detail'),
]
