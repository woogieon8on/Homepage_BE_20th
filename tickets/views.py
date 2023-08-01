from django.shortcuts import render
from functools import partial
from django import forms
from django.core.exceptions import ValidationError

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import GeneralTicket, FreshmanTicket, Participant, OrderTransaction
from .serializers import GeneralTicketDetailSerializer

# import traceback

#serializer에 partial=True를 주기위한 Mixin
class SetPartialMixin:
    def get_serializer_class(self, *args, **kwargs):
        serializer_class = super().get_serializer_class(*args, **kwargs)
        return partial(serializer_class, partial=True)


class GeneralTicketOrderView(viewsets.ModelViewSet):
    queryset = GeneralTicket.objects.all()
    serializer_class = GeneralTicketDetailSerializer
    permission_classes = (AllowAny, )

    class Meta:
        examples = {
            'buyer': '깔루아1',
            'phone_num': '010-1234-5678',
            'member': '3',
            'price': '15000',
            'name': '깔루아1',
            'phone': '010-1234-5678',
            'name': '깔루아2',
            'phone': '010-8765-4321',
            'name': '깔루아3',
            'phone': '010-5678-1234',
        }

    @swagger_auto_schema(
        operation_id='티켓 구매 관련 정보 입력(주문서 입력)',
        operation_description='''
            티켓을 구매하는 사람이 구매자 이름, 전화번호, 예매인원 등의 정보를 입력합니다.<br/>
            예매 금액을 책정해서 iamport에 넘겨주어야 함</br>
            참고로 request body는 json 형식이 아닌 <b>multipart/form-data 형식</b>으로 전달받으므로, 
            리스트 값을 전달하고자 한다면 개별 원소들마다 리스트 필드 이름을 key로 설정하여, 원소 값을 value로 추가해주면 됩니다.<br/>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {'id': 1}
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        order_info = request.data
        name_list = order_info.getlist('name')
        phone_list = order_info.getlist('phone')
        
        serializer = self.get_serializer(data=order_info)
        if serializer.is_valid():
            new_order = serializer.save()

            mem = dict(zip(name_list, phone_list))

            for key, value in mem.items():
                mem = Participant(name=key, phone_num=value, general_ticket=new_order)
                mem.save()
        
            return Response({
                'status': 'success',
                'data': new_order.id,
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status':'error',
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_id='주문이 완료된 후 표시하는 View',
        operation_description='''
            결제를 하고 나서 주문이 완료되었다는 화면을 표시할 때 사용됩니다.<br/>
            주문 번호에 해당하는 결제 완료 화면을 보여줍니다.<br/>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {'id': 1,
                                 'buyer':'깔루아1',
                                 'phone_num':'010-1234-5678',
                                 'member':'3',
                                 'price':'15000'
                                }
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }
    )
    def get(self, request):
        order_id = request.query_params.get('order_id')
        order = GeneralTicket.objects.get(id=order_id)
        serializer = self.get_serializer(order)
        
        return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
    

class OrderCheckoutView(viewsets.ModelViewSet):
    permission_classes = (AllowAny, )

    class Meta:
        examples = {
            'order_id': 1,
            'amount': 15000,
        }

    @swagger_auto_schema(
        operation_id='OrderTransaction 객체를 생성하는 view',
        operation_description='''
            전달된 필드를 기반으로 결제 정보를 저장할 때 사용하는 OrderTransaction 객체를 생성합니다.<br/>
            이때 merchant_order_id을 생성하여 반환받아서 다음 절차에 사용합니다.<br/>          
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {'id': 1}
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }
    )

    def post(self, request, *args, **kwargs):
        ticket_id = request.POST.get('ticket_id')
        order = GeneralTicket.objects.get(id=ticket_id)
        amount = request.POST.get('amount')

        try:
            merchant_order_id = OrderTransaction.objects.create_new(
                order=order,
                amount=amount,
            )
        except:
            merchant_order_id = None
            # print(traceback.format_exc())
    
        if merchant_order_id is not None:
            return Response({
                'status': True,
                'merchant_order_id': merchant_order_id,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'fail',
                'message': '주문번호가 존재하지 않습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)


class OrderValidationView(viewsets.ModelViewSet):
    class Meta:
        examples = {
            'order_id': 1,
            'merchant_id': '2abcdefghi',
            'imp_id': '',
            'amount': 15000,
        }

    @swagger_auto_schema(
        operation_id='실제 결제가 끝난 뒤에 결제를 검증하는 View',
        operation_description='''
            결제 검증까지 마치고 나면 order_complete 뷰를 호출해 주문이 완료되었음을 표시하고 전체 절차를 마칩니다.<br/>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }

    )

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        order = GeneralTicket.objects.get(id=order_id)
        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')
        
        try:
            trans = OrderTransaction.objects.get(
                order=order,
                merchant_order_id=merchant_id,
                amount=amount,
            )
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            trans.success = True
            trans.save()
            
            return Response({
                'status':'success',
            },status=status.HTTP_200_OK)

# 구매자 정보 조회는 로그인 시에만 가능