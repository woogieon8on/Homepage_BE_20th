from django.urls import path
from .views import FreshmanTicketOrderView, GeneralTicketOrderView, OrderCheckoutView, OrderValidationView

app_name = 'tickets'

urlpatterns = [
    path('general_ticket/', GeneralTicketOrderView.as_view({'post':'create'}), name='general_ticket'),
    path('freshman_ticket/', FreshmanTicketOrderView.as_view({'post':'create'}), name='freshman_ticket'),
    path('checkout/', OrderCheckoutView.as_view({'post':'post'}), name='order_checkout'),
    path('validation/', OrderValidationView.as_view({'post':'post'}), name='order_validation'),
    path('complete/', GeneralTicketOrderView.as_view({'get':'get'}), name='order_complete'),
]