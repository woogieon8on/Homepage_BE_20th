from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from application.models import ApplyForm  # "application"은 지원서를 만드는 모델이 있는 앱 이름입니다.
from ..serializers.application_serializers import ApplyFormListSerializer, ApplyFormDetailSerializer

class ApplicationsPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'

# 지원한 애들 정보 관리자페이지에서 볼 수 있게
class ApplicationRetrieveView(viewsets.ModelViewSet):
    """
        지원서에서 name, phone_num, birthdate, first_preference, second_preference만 리스트로 가져오기
    """
    queryset = ApplyForm.objects.all().order_by('id')
    serializer_class = ApplyFormListSerializer # ApplyFormListSerializer(위 속성만)에서 가져옴
    permission_classes = [IsAuthenticated]
    pagination_class = ApplicationsPagination
    
    @swagger_auto_schema(
        operation_id='지원서 리스트 가져오기',
        operation_description='''
            지원서 작성 후 지원서 정보를 조회할 화면을 표시할 때 사용됩니다.<br/>
            주문 번호에 해당하는 지원서 화면을 보여줍니다.<br/>
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
                                 'first_preference': '기타',
                                 'second_preference': '신디',
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
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 'Success',
            'data': response.data,
        }, status=status.HTTP_200_OK)
    
# detail 볼 수 있게
class ApplicationRetrieveDetailView(viewsets.ModelViewSet):
    """
        해당 id값에 따른 모든 세부 정보(detail) 보이기
    """
    queryset = ApplyForm.objects.all().order_by('id')
    serializer_class = ApplyFormDetailSerializer # ApplyFormDetailSerializer('__all__)'에서 가져옴
    permission_classes = [IsAuthenticated]
    pagination_class = ApplicationsPagination

    @swagger_auto_schema(
        operation_id='지원서 id값에 따른 디테일 모두 가져오기',
        operation_description='''
            id값에 해당하는 지원서의 모든 내용을 보여줍니다.<br/>
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "Success",
                        "data": {"id": 1,
                                 "created": "2023-11-15T07:14:34.728497Z",
                                 "updated": "2023-11-15T07:14:34.728497Z",
                                 "name": "깔루아1",
                                 "phone_num": "010-6337-5958",
                                 "birthdate": "2002-05-31",
                                 "gender": "남성",
                                 "address": "마포구",
                                 "first_preference": "기타",
                                 "second_preference": "신디",
                                 "play_instrument": "기타",
                                 "motive": "깔루아 들어가고 싶어요",
                                }
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        }
    )

    def applydetail(self, request):
        try:
            id = request.GET['id'] # 프론트에서 받아옴
            detail_application = get_object_or_404(ApplyForm.objects.all(), id=id)
            serializer = ApplyFormDetailSerializer(detail_application)

            return Response({
                'status': 'Success',
                'data' : serializer.data,
            }, status=status.HTTP_200_OK) 
        
        except ValueError as ve:
            return Response({
                'status': 'Error',
                'error_message': str(ve),
            }, status=status.HTTP_400_BAD_REQUEST)