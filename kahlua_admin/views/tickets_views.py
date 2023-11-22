from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from tickets.models import FreshmanTicket, OrderTransaction, Participant
from ..serializers.tickets_serializers import FreshmanAdminSerializer, GeneralTicketAdminListSerializer


class TicketsPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'


class FreshmanViewSet(viewsets.ModelViewSet):
    """
        새내기 티켓 예약 리스트 가져오기
    """
    queryset = FreshmanTicket.objects.all().order_by('id')  #예약 순서대로 정렬
    serializer_class = FreshmanAdminSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TicketsPagination

    @swagger_auto_schema(operation_id='신입생 예매 티켓 리스트 가져오기')
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 'Success',
            'data': response.data,
        }, status=status.HTTP_200_OK)
    

class GeneralTicketListViewSet(viewsets.ModelViewSet):
    """
        일반 티켓 예매 정보 가져오기
    """
    queryset = OrderTransaction.objects.all().order_by('id')
    serializer_class = GeneralTicketAdminListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TicketsPagination

    @swagger_auto_schema(operation_id='일반 예매 티켓 리스트 가져오기')
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 'Success',
            'data': response.data,
        }, status=status.HTTP_200_OK)


# class GeneralDto:
#     id: int
#     buyer: str
#     phone_num: str
#     member: int
    # participants: list[dict]


# class GeneralTicketDetailViewSet(viewsets.ModelViewSet):
#     """
#         일반 티켓 상세 정보 가져오기
#     """
#     queryset = OrderTransaction.objects.all().order_by('id')
#     serializer_class = GeneralTicketAdminDetailSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = TicketsPagination
    
#     @swagger_auto_schema(operation_id='일반 예매 티켓 디테일 가져오기')
#     def get(self,request):
#         id = request.query_params.get('id')
#         print('id:', id)
#         ticket = OrderTransaction.objects.select_related('order').get(id=id)
#         print('tickett:', ticket.order.member)

#         ticket_dto = GeneralDto(
#             id=ticket.id,
#             buyer=ticket.order.buyer,
#             phone_num=ticket.order.phone_num,
#             member=ticket.order.member,
#             # participants=[{'name': participant.name, 'phone': participant.phone}
#             #               for participant in ticket.participants.all()]
#         )
#         print('dto', ticket_dto)
#         return ticket_dto


#         # # detail_ticket = get_object_or_404(self.get_queryset(), pk=id)
#         # # print('detail_', detail_ticket)
#         # ticket = self.get_queryset().get(id=id)
#         # print('de::', Participant.objects.filter(general_ticket=ticket))

#         # serializer = self.get_serializer(ticket)
#         # print('ser:', serializer)

#         # return Response({
#         #     'status': 'Success',
#         #     'data': serializer.data,
#         #     }, status=status.HTTP_200_OK)
    
#         # # return Response({
#         # #     'status': 'error',
#         # # }, status=status.HTTP_400_BAD_REQUEST)