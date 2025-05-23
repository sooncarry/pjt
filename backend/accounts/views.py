from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import FinancialProfile
from .serializers import FinancialProfileSerializer
from django.utils import timezone


User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny]) 
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': '회원가입 성공'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])  # ✅ 추가
def check_username(request):
    username = request.GET.get('username')
    is_taken = User.objects.filter(username=username).exists()
    return JsonResponse({'is_taken': is_taken})


class MyPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def financial_profile_view(request):
    user = request.user
    if request.method == 'GET':
        try:
            profile = FinancialProfile.objects.get(user=user)
            serializer = FinancialProfileSerializer(profile)
            return Response(serializer.data)
        except FinancialProfile.DoesNotExist:
            return Response({'checklist_submitted': False})
    
    if request.method == 'POST':
        # request.data: { saving_score: 6, spending_score: 2 }
        saving_score = int(request.data.get('saving_score', 0))
        spending_score = int(request.data.get('spending_score', 0))

        # 성향 결정 로직
        def get_style(score):
            if score <= 2:
                return '보수적'
            elif score <= 4:
                return '중립적'
            return '공격적'
        
        saving_style = get_style(saving_score)
        spending_style = get_style(spending_score)

        # 칭호 매핑
        title_map = {
            ('보수적', '보수적'): '재무 도인',
            ('보수적', '중립적'): '현실 재테커',
            ('보수적', '공격적'): '불안한 소비자',
            ('중립적', '보수적'): '계획형 실속러',
            ('중립적', '중립적'): '밸런스 마스터',
            ('중립적', '공격적'): '지름신과 동행 중',
            ('공격적', '보수적'): '절제된 야망가',
            ('공격적', '중립적'): '준야수형 자산가',
            ('공격적', '공격적'): '하이리스크 하이리턴러',
        }

        title = title_map.get((spending_style, saving_style), '미지정')

        profile, created = FinancialProfile.objects.get_or_create(user=user)
        profile.saving_style = saving_style
        profile.spending_style = spending_style
        profile.title = title
        profile.checklist_submitted = True
        profile.save()

        serializer = FinancialProfileSerializer(profile)
        return Response(serializer.data)
    
