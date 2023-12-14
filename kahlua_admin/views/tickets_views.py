from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, serializers
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
    queryset = FreshmanTicket.objects.all().order_by('-id')  #예약 순서대로 정렬
    serializer_class = FreshmanAdminSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TicketsPagination

    @swagger_auto_schema(operation_id='신입생 예매 티켓 리스트 가져오기')
    def list(self, request, *args, **kwargs):
        order = self.get_queryset()
        latest = request.GET.get('latest', False)
        if latest:
            order = FreshmanTicket.objects.all().order_by('buyer')
        serializer = self.get_serializer(order, many=True)

        return Response({
            'status': 'Success',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)
    

class GeneralTicketListViewSet(viewsets.ModelViewSet):
    """
        일반 티켓 예매 정보 가져오기
    """
    queryset = OrderTransaction.objects.all().order_by('-id')
    serializer_class = GeneralTicketAdminListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TicketsPagination

    @swagger_auto_schema(operation_id='일반 예매 티켓 리스트 가져오기')
    def list(self, request, *args, **kwargs):
        order = self.get_queryset()
        latest = request.GET.get('latest', False)
        if latest:
            order = OrderTransaction.objects.all().order_by('order__buyer')
        serializer = self.get_serializer(order, many=True)

        return Response({
            'status': 'Success',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)
