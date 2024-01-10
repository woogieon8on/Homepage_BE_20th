from django.urls import path
from .views.views import FreshmanTicketOrderView, GeneralTicketOrderView, OrderCheckoutView, OrderValidationView, CancelTicketView

app_name = 'tickets'

urlpatterns = [
    path('general_ticket/', GeneralTicketOrderView.as_view({'post':'create'}), name='general_ticket'),
    path('freshman_ticket/', FreshmanTicketOrderView.as_view({'post':'create'}), name='freshman_ticket'),
    path('freshman_complete/', FreshmanTicketOrderView.as_view({'get':'get'}), name = 'freshman_complete'),
    path('freshman_ticket/delete/', FreshmanTicketOrderView.as_view({'delete':'delete'}), name='delete_freshman'),
    path('checkout/', OrderCheckoutView.as_view({'post':'post'}), name='order_checkout'),
    path('validation/', OrderValidationView.as_view({'post':'post'}), name='order_validation'),
    path('general_complete/', GeneralTicketOrderView.as_view({'get':'get'}), name='general_complete'),
    path('general_ticket/delete/', CancelTicketView.as_view({'delete':'delete'}), name='delete'),
]