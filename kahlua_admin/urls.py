from django.urls import path
from .views.tickets_views import FreshmanViewSet, GeneralTicketListViewSet
from .views.application_views import ApplicationRetrieveView, ApplicationRetrieveDetailView

app_name = 'kahlua_admin'

urlpatterns = [
    path('tickets/freshman_tickets/', FreshmanViewSet.as_view({'get':'list'}), name='freshman_list'),
    path('tickets/general_tickets/list/', GeneralTicketListViewSet.as_view({'get':'list'}), name='general_list'),
    # path('tickets/general_tickets/detail/', GeneralTicketDetailViewSet.as_view({'get':'get'}), name='general_detail'),
    path('application/apply_forms/', ApplicationRetrieveView.as_view({'get':'list'}), name='apply_forms_list'),
    path('application/apply_forms/applydetail/', ApplicationRetrieveDetailView.as_view({'get':'applydetail'}), name='apply_forms_detail'),
]
