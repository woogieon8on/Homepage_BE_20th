from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from application.models import ApplyForm
from application.serializers import ApplyFormCreateSerializer


class ApplyCreateView(CreateAPIView):
    model = ApplyForm
    serializer_class = ApplyFormCreateSerializer
    permission_classes = (AllowAny, )

    class Meta:
        examples = {
            'name': '깔루아1',
            'phone_num':'010-1234-5678',
            'birthdate': '2002-05-31',
            'gender': '여성',
            'address': '서울특별시 마포구',
            'first_preference': '기타',
            'second_preference': '신디',
            'play_instrument': '기타는 1년 정도 독학했습니다.',
            'motive': '깔루아와 함께 즐거운 대학생활을 하고 싶습니다.',
        }

    @swagger_auto_schema(
        operation_id='지원서 작성',
        operation_description='''
            지원서를 작성합니다. 생년월일의 경우 '0000-00-00'의 형태를 맞춰줘야 합니다.<br/>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {'id': 1,
                                 'name':'깔루아1',
                                 'phone_num':'010-6337-5958',
                                 'birthdate':'2002-05-31',
                                 'gender': '여성',
                                 'address': '서울특별시 마포구',
                                 'first_preference': '기타',
                                 'second_preference': '신디',
                                 'play_instrument': '기타는 1년 정도 독학했습니다.',
                                 'motive': '깔루아와 함께 즐거운 대학생활을 하고 싶습니다.',
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
            print('save')

            return Response({
                'status': 'Success',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status':'error'
        }, status=status.HTTP_400_BAD_REQUEST)