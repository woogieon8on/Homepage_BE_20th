from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from application.models import ApplyForm
from application.serializers import ApplyFormCreateSerializer, ApplyFormCompleteSerializer


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
        request_body=openapi.Schema(
            '지원서 작성',
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema('지원자 성함', type=openapi.TYPE_STRING),
                'phone_num': openapi.Schema('지원자 전화번호', type=openapi.TYPE_NUMBER),
                'birthdate': openapi.Schema('생년월일', type=openapi.TYPE_STRING),
                'gender': openapi.Schema('성별', type=openapi.TYPE_STRING, enum=['남성', '여성']),
                'address': openapi.Schema('거주지', type=openapi.TYPE_STRING),
                'major': openapi.Schema('전공학과', type=openapi.TYPE_STRING, enum=['컴퓨터공학과', '자율전공학과']),
                'first_preference': openapi.Schema('1지망', type=openapi.TYPE_STRING, enum=['보컬', '드럼', '기타', '베이스', '신디(피아노)']),
                'second_preference': openapi.Schema('2지망', type=openapi.TYPE_STRING, enum=['보컬', '드럼', '기타', '베이스', '신디(피아노)']),
                'experience_and_reason': openapi.Schema('지원세션 경력과 이유', type=openapi.TYPE_STRING),
                'play_instrument': openapi.Schema('다룰 줄 아는 악기', type=openapi.TYPE_STRING),
                'motive': openapi.Schema('지원동기', type=openapi.TYPE_STRING),
                'finish_time': openapi.Schema('수업 끝나는 시간', type=openapi.TYPE_STRING),
                'meeting': openapi.Schema('뒷풀이 참석 여부', type=openapi.TYPE_BOOLEAN),
                'readiness': openapi.Schema('면접 전 각오', type=openapi.TYPE_STRING)
            }
        ),
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

            return Response({
                'status': 'Success',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status':'error'
        }, status=status.HTTP_400_BAD_REQUEST)
    

class ApplyCompleteView(APIView):
    model = ApplyForm
    serializer_class = ApplyFormCompleteSerializer
    permission_classes = (AllowAny, )

    @swagger_auto_schema(
        operation_id='지원서 작성 완료 후 확인 페이지',
        operation_description='''
            지원이 완료된 후 query parameter로 id값을 넘겨주면 id 값에 해당하는 지원서를 보여줍니다.</br>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "Success",
                        "data": {
                            'id': 1,
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
            id = request.query_params.get('id')
            request = ApplyForm.objects.get(id=id)
            serializer = ApplyFormCompleteSerializer(instance=request)

            return Response({
                'status': 'Success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except:
            return Response({
                'status': 'error',
            }, status=status.HTTP_400_BAD_REQUEST)