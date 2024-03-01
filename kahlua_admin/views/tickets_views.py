from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from itertools import chain
from operator import attrgetter
from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from tickets.models import FreshmanTicket, GeneralTicket, OrderTransaction, Participant
from ..serializers.tickets_serializers import FreshmanAdminSerializer, GeneralTicketAdminListSerializer


class TicketsPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'


class FreshmanViewSet(viewsets.ModelViewSet):
    queryset = FreshmanTicket.objects.all().order_by('-id')  #예약 순서대로 정렬
    serializer_class = FreshmanAdminSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TicketsPagination

    @swagger_auto_schema(
        operation_id='신입생 티켓 예약 리스트 가져오기',
        operation_description='''
            모든 신입생 티켓을 리스트로 불러옵니다.<br/>
            기본 정렬은 최신이 가장 위로 올라오도록 정렬됩니다. query params에서 name을 True로 설정하면 이름 순으로 정렬됩니다.<br/>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {
                            "total_freshman": 1,
                            "tickets": {
                                "id": 1,
                                "buyer": "kahlua",
                                "phone_num": "01012345678",
                                "count": 1,
                                "major": "컴퓨터공학과",
                                "student_id": "C41111",
                                "meeting": True,
                                "reservation_id": "04LQMHA43W"
                            },
                        }
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        order = self.get_queryset()
        order_name = request.GET.get('name', False)
        if order_name:
            order = FreshmanTicket.objects.all().order_by('buyer')

        total_freshman = FreshmanTicket.objects.aggregate(count_sum=Sum('count'))['count_sum']

        serializer = self.get_serializer(order, many=True)

        return Response({
            'status': 'Success',
            'data': {
                'total_freshman': total_freshman,
                'tickets': serializer.data,
            },
        }, status=status.HTTP_200_OK)
    

class GeneralTicketListViewSet(viewsets.ModelViewSet):
    queryset = OrderTransaction.objects.all().order_by('-id')
    serializer_class = GeneralTicketAdminListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TicketsPagination

    @swagger_auto_schema(
        operation_id='일반 티켓 예매 정보 가져오기',
        operation_description='''
            모든 일반 티켓을 리스트로 불러옵니다.<br/>
            기본 정렬은 최신이 가장 위로 올라오도록 정렬됩니다. query params에서 name을 True로 설정하면 이름 순으로 정렬됩니다.<br/>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {
                            "total_general": 1,
                            "tickets": {
                                "id": 1,
                                "buyer": "kahlua",
                                "phone_num": "01012345678",
                                "member": 2,
                                "merchant_order_id": "734ea4eadf",
                                "transaction_status": "paid",
                                "participants": "[{'name': '깔루아', 'phone_num': '01012345678'}, {'name': '깔루아', 'phone_num': '01012345678'}]",
                            },
                        }
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        order = self.get_queryset()
        order_name = request.GET.get('name', False)  # 이름순 정렬
        if order_name:
            order = OrderTransaction.objects.all().order_by('order__buyer')

        total_general = GeneralTicket.objects.aggregate(member_sum=Sum('member'))['member_sum']

        serializer = self.get_serializer(order, many=True)

        return Response({
            'status': 'Success',
            'data': {
                'total_general': total_general,
                'tickets': serializer.data,
            },
        }, status=status.HTTP_200_OK)


class AllTicketListViewSet(viewsets.ModelViewSet):
    serializer_class_General = GeneralTicketAdminListSerializer
    serializer_class_Freshman = FreshmanAdminSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TicketsPagination

    @swagger_auto_schema(
        operation_id='모든 티켓 예매 정보 가져오기',
        operation_description='''
            모든 티켓을 리스트로 불러옵니다.<br/>
            기본 정렬은 최신이 가장 위로 올라오도록 정렬됩니다. query params에서 name을 True로 설정하면 이름 순으로 정렬됩니다.<br/>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "Success",
                        "data": {
                            "total_tickets": 4,
                            "tickets": [
                                {
                                    "id": 1,
                                    "buyer": "깔루아",
                                    "phone_num": "01012345678",
                                    "count": 1,
                                    "major": "컴퓨터공학과",
                                    "student_id": "c111111",
                                    "meeting": True,
                                    "reservation_id": "04LQMHA43W"
                                },
                                {
                                    "id": 2,
                                    "buyer": "kahlua",
                                    "phone_num": "01011001234",
                                    "member": 3,
                                    "merchant_order_id": "d561280932",
                                    "transaction_status": "paid"
                                },
                            ]
                        }
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }
    )

    def list(self, request, *args, **kwargs):
        general = OrderTransaction.objects.all()
        freshman = FreshmanTicket.objects.all()

        combined_data = sorted(
            chain(general, freshman),
            key=attrgetter('created'),  #'create_at'의 속성으로 정렬
            reverse=True
        )
        
        data = []
        for item in combined_data:
            if isinstance(item, OrderTransaction):
                serializer = self.serializer_class_General(item)
            elif isinstance(item, FreshmanTicket):
                serializer = self.serializer_class_Freshman(item)
            else:
                continue

            data.append(serializer.data)
        
        total_freshman = FreshmanTicket.objects.aggregate(count_sum=Sum('count'))['count_sum']
        total_general = GeneralTicket.objects.aggregate(member_sum=Sum('member'))['member_sum']
        total_tickets = total_freshman + total_general

        return Response({
            'status':'Success',
            'data' : {
                'total_tickets': total_tickets,
                'tickets': data,
            },
        }, status=status.HTTP_200_OK)