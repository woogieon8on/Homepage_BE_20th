from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from tickets.models import FreshmanTicket
from ..serializers.tickets_serializers import FreshmanSerializer


class TicketsPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'


class FreshmanViewSet(viewsets.ModelViewSet):
    """
        모든 티켓 예약 리스트 가져오기
    """
    queryset = FreshmanTicket.objects.all().order_by('id')  #예약 순서대로 정렬
    serializer_class = FreshmanSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TicketsPagination

    @swagger_auto_schema(operation_id='신입생 예매 티켓 리스트 가져오기')
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 'Success',
            'data': response.data,
        }, status=status.HTTP_200_OK)