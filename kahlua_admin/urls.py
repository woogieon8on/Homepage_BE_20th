from django.urls import path
<<<<<<< Updated upstream
from .views.tickets_views import FreshmanViewSet, GeneralTicketListViewSet
from .views.application_views import ApplicationViewSet
=======
from .views.tickets_views import FreshmanViewSet, GeneralTicketListViewSet, AllTicketListViewSet
>>>>>>> Stashed changes

app_name = 'kahlua_admin'

urlpatterns = [
    path('tickets/freshman_tickets/', FreshmanViewSet.as_view({'get':'list'}), name='freshman_list'),
    path('tickets/general_tickets/', GeneralTicketListViewSet.as_view({'get':'list'}), name='general_list'),
<<<<<<< Updated upstream
    path('application/apply_forms/', ApplicationViewSet.as_view({'get':'list'}), name='applyforms_list'),    
]
=======
    path('tickets/all/', AllTicketListViewSet.as_view({'get':'list'}), name='all_list'),
]
>>>>>>> Stashed changes
