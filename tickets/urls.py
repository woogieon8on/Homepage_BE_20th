from django.urls import path
from .views import GeneralTicketOrderView

app_name = 'tickets'

urlpatterns = [
    path('general_ticket/', GeneralTicketOrderView.as_view({'post':'create'}), name='general_ticket'),
    # path('checkout/', OrderCheckoutView.as_view({'post':'post'}), name='order_checkout'),
    # path('complete/', OrderCompleteView.as_view({'post':'post'}), name='order_complete'),
]