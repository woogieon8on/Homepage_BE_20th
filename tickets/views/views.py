from django.shortcuts import render
from functools import partial
from django import forms
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from tickets.models import GeneralTicket, FreshmanTicket, Participant, OrderTransaction
from tickets.serializers import GeneralTicketDetailSerializer, FreshmanTicketDetailSerializer
from tickets.views.send_msg import send_message

import traceback

#serializer에 partial=True를 주기위한 Mixin
class SetPartialMixin:
    def get_serializer_class(self, *args, **kwargs):
        serializer_class = super().get_serializer_class(*args, **kwargs)
        return partial(serializer_class, partial=True)


@method_decorator(csrf_exempt, name='dispatch')
class FreshmanTicketOrderView(viewsets.ModelViewSet):
    queryset = FreshmanTicket.objects.all()
    serializer_class = FreshmanTicketDetailSerializer
    permission_classes = (AllowAny, )

    class Meta:
        examples = {
            'buyer': '신입생1',
            'phone_num': '010-1234-5678',
            'major': '컴퓨터공학과',
            'student_id': 'C411111',
            'meeting': True,
        }

    @swagger_auto_schema(
        operation_id='신입생 티켓 구매 관련 정보 입력',
        operation_description='''
            신입생의 경우 1인 1매로 제한되므로 예매자의 정보만 입력받고 있습니다.<br/>
            신입생 확인을 위해 예매 시 학과와 학번을 입력 받고, 현장에서 학생증으로 학과와 학번이 맞는지 확인합니다.<br/>
        ''',
        request_body=openapi.Schema(
            '신입생 티켓 정보 입력',
            type=openapi.TYPE_OBJECT,
            properties={
                'buyer': openapi.Schema('구매자 이름', type=openapi.TYPE_STRING),
                'phone_num': openapi.Schema('구매자 전화번호', type=openapi.TYPE_NUMBER),
                'major': openapi.Schema('전공', type=openapi.TYPE_INTEGER),
                'student_id': openapi.Schema('학번', type=openapi.TYPE_STRING),
                'meeting': openapi.Schema('소모임 참석여부', type=openapi.TYPE_STRING)
            }
        ),
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {'id': 1,
                                 'buyer': '신입생1',
                                 'phone_num': '010-1234-5678',
                                 'major': '컴퓨터공학과',
                                 'student_id': 'C411111',
                                 'meeting': '3/5',
                                 'reservation_id': '12345ABCDE'
                                }
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({
                'status': 'success',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status':'error',
        }, status=status.HTTP_400_BAD_REQUEST) 


    @swagger_auto_schema(
        operation_id='신입생 예매 확인',
        operation_description='''
            query parameter로 입력받은 reservation_id에 해당하는 티켓을 보여줍니다. <br/>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {'id': 1,
                             'buyer': '신입생1',
                             'phone_num': '010-1234-5678',
                             'major': '컴퓨터공학과',
                             'student_id': 'C411111',
                             'meeting': True,
                             'reservation_id': '12345ABCDE'
                            }
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            reservation_id = request.query_params.get('reservation_id')
            request = FreshmanTicket.objects.get(reservation_id=reservation_id)
            serializer = self.get_serializer(request)

            return Response({
                'status': 'Success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        except:
            return Response({
                'status': 'error',
            }, status=status.HTTP_400_BAD_REQUEST)
    
    
    @swagger_auto_schema(
        operation_id='신입생 예매 취소',
        operation_description='''
            student_id와 reservation_id가 모두 일치하는 경우 해당 freshman tickets을 삭제하면서 예매를 취소한다. <br/>
        ''',
        request_body=openapi.Schema(
            '신입생 티켓 삭제',
            type=openapi.TYPE_OBJECT,
            properties={
                'student_id': openapi.Schema('학번', type=openapi.TYPE_STRING),
                'reservation_id': openapi.Schema('예약번호', type=openapi.TYPE_STRING)
            }
        ),
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

    def delete(self, request, *args, **kwargs):   
        # student_id = request.POST.get('student_id')
        reservation_id = request.POST.get('reservation_id')

        try:
            student = FreshmanTicket.objects.get(reservation_id=reservation_id)
            print('stu:', student)
            student.delete()

            return Response({
                'status':'success',
            },status=status.HTTP_200_OK)

        except FreshmanTicket.DoesNotExist:
            student = None

            return Response({
                'status': 'fail',
                'message': '학번이 존재하지 않습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)


        

# @method_decorator(csrf_exempt, name='dispatch')
class GeneralTicketOrderView(viewsets.ModelViewSet):
    queryset = GeneralTicket.objects.all()
    serializer_class = GeneralTicketDetailSerializer
    permission_classes = (AllowAny, )

    class Meta:
        examples = {
            'buyer': '깔루아1',
            'phone_num': '010-1234-5678',
            'member': '3',
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
        request_body=openapi.Schema(
            '티켓 구매 관련 정보 입력',
            type=openapi.TYPE_OBJECT,
            properties={
                'buyer': openapi.Schema('구매자 이름', type=openapi.TYPE_STRING),
                'phone_num': openapi.Schema('구매자 전화번호', type=openapi.TYPE_NUMBER),
                'member': openapi.Schema('참석인원', type=openapi.TYPE_INTEGER),
                'name': openapi.Schema('참석자 이름', type=openapi.TYPE_OBJECT),
                'phone': openapi.Schema('참석자 전화번호', type=openapi.TYPE_OBJECT),
                'payment': openapi.Schema('결제 수단', type=openapi.TYPE_STRING),
            }
        ),
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
                                 'price':'15000',
                                 'payment': '계좌이체',
                                 'status': False,
                                },
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        order_info = request.POST.copy()
        name_list = order_info.getlist('name[]')
        phone_list = order_info.getlist('phone[]')

        # if order_info['payment'] == '카카오페이':
        #     order_info['status'] = True

        serializer = self.get_serializer(data=order_info) 
        if serializer.is_valid(raise_exception=True):
            new_order = serializer.save()

            mem = dict(zip(name_list, phone_list))

            for key, value in mem.items():
                mem = Participant(name=key, phone_num=value, general_ticket=new_order)
                mem.save()

            return Response({
                'status': 'success',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status':'error',
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_id='주문이 완료된 후 표시 & 예매 티켓 조회',
        operation_description='''
            전달된 쿼리 파라미터에 해당하는 예매 정보를 반환합니다.<br/>
            결제를 하고 나서 주문이 완료되었다는 화면을 표시할 때 사용됩니다.<br/>
            또는 예매 티켓을 조회하는 경우 예매번호(merchant_order_id)를 입력하여 예매 내역을 확인합니다.<br/>
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
                                 'price':'15000',
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
        try:
            request_id = request.query_params.get('merchant_order_id')
            request = OrderTransaction.objects.get(merchant_order_id=request_id)
            serializer = self.get_serializer(request.order)
            
            return Response({
                'status': 'Success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        except:
            return Response({
                'status': 'error',
            }, status=status.HTTP_400_BAD_REQUEST)
    

@method_decorator(csrf_exempt, name='dispatch')
class OrderCheckoutView(viewsets.ModelViewSet):
    permission_classes = (AllowAny, )

    class Meta:
        examples = {
            'amount': 15000,
        }

    @swagger_auto_schema(
        operation_id='OrderTransaction 객체를 생성하는 view',
        operation_description='''
            전달된 필드를 기반으로 결제 정보를 저장할 때 사용하는 OrderTransaction 객체를 생성합니다.<br/>
            이때 merchant_order_id을 생성하여 반환받아서 다음 절차에 사용합니다.<br/>          
        ''',
        request_body=openapi.Schema(
            '결제 정보 객체 생성',
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema('예약번호', type=openapi.TYPE_STRING),
                'amount': openapi.Schema('가격', type=openapi.TYPE_NUMBER),
            }
        ),
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {'merchant_order_id': '2abcdefghi'}
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }
    )

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        order = GeneralTicket.objects.get(id=id)
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


@method_decorator(csrf_exempt, name='dispatch')
class OrderValidationView(viewsets.ModelViewSet):
    permission_classes = (AllowAny, )
    
    class Meta:
        examples = {
            'merchant_id': '2abcdefghi',
            'imp_id': '',
            'amount': 15000,
        }

    @swagger_auto_schema(
        operation_id='실제 결제가 끝난 뒤에 결제를 검증하는 View',
        operation_description='''
            결제 검증까지 마치고 나면 order_complete 뷰를 호출해 주문이 완료되었음을 표시하고 전체 절차를 마칩니다.<br/>
        ''',
        request_body=openapi.Schema(
            '결제 검증',
            type=openapi.TYPE_OBJECT,
            properties={
                'merchant_id': openapi.Schema('주문번호', type=openapi.TYPE_STRING),
                'imp_id': openapi.Schema('아임포트 id', type=openapi.TYPE_STRING),
                'amount': openapi.Schema('가격', type=openapi.TYPE_NUMBER),
            }
        ),
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
        # reservation_id = request.POST.get('reservation_id')
        # order = GeneralTicket.objects.get(reservation_id=reservation_id)
        merchant_order_id = request.POST.get('merchant_order_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        # participants = Participant.objects.filter(general_ticket=order.id)
        
        try:
            trans = OrderTransaction.objects.get(
                merchant_order_id=merchant_order_id,
                amount=amount,
            )
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            trans.success = True
            trans.save()

            send_message(name=trans.order.buyer, phone_num=trans.order.phone_num)

            # 참석자 전원에게 문자 보내는 경우
            # for participant in participants:
            #     send_message(name=participant.name, phone_num=participant.phone_num)
            
            return Response({
                'status':'success',
            },status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class CancelTicketView(viewsets.ModelViewSet):
    permission_classes = (AllowAny, )

    class Meta:
        examples = {
            'merchant_order_id': '12345abcde',
        }

    @swagger_auto_schema(
        operation_id='일반 예매 취소하는 View',
        operation_description='''
            merchant_order_id에 해당하는 general tickets를 삭제하고 participants 해당 인원 모두 삭제한다.
            또한 order transactions 모두 삭제하면서 예매를 취소한다. <br/>
        ''',
        request_body=openapi.Schema(
            '티켓 취소',
            type=openapi.TYPE_OBJECT,
            properties={
                'merchant_order_id': openapi.Schema('주문번호', type=openapi.TYPE_STRING),
            }
        ),
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

    def delete(self, request, *args, **kwargs):
        merchant_order_id = request.POST.get('merchant_order_id')
        order = OrderTransaction.objects.get(merchant_order_id=merchant_order_id)
        
        try:
            trans = GeneralTicket.objects.get(
                id=order.order.id,
            )
        except:
            trans = None

        if trans is not None:
            participant = trans.participants.all()
            participant.delete()
            order.delete() 
            trans.delete()
            
            return Response({
                'status':'success',
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'fail',
                'message': '주문번호가 존재하지 않습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
