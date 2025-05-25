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

# 이메일 인증 구현 용
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import EmailVerificationTokenGenerator
from django.contrib.sites.shortcuts import get_current_site


User = get_user_model()
token_generator = EmailVerificationTokenGenerator()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': '회원가입 성공'}, status=201)
    return Response(serializer.errors, status=400)

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
    

class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': '이메일 인증 성공! 이제 로그인할 수 있습니다.'}, status=200)
        else:
            return Response({'error': '유효하지 않거나 만료된 링크입니다.'}, status=400)
        

# views.py
from django.utils.crypto import get_random_string

@api_view(['POST'])
@permission_classes([AllowAny])
def send_verification_email(request):
    email = request.data.get('email')
    name = request.data.get('name', '')

    if not email:
        return Response({'detail': '이메일이 필요합니다.'}, status=400)

    # 항상 새로운 임시 유저 생성
    base_username = email.split('@')[0]
    final_username = f"{base_username}_{get_random_string(6)}"

    user = User.objects.create(
        username=final_username,
        email=email,
        is_active=False,
        first_name=name
    )
    user.set_password(User.objects.make_random_password())
    user.save()

    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    activate_url = f"http://localhost:5173/signup?uidb64={uidb64}&token={token}"

    subject = '[부자되자] 이메일 인증 요청'
    message = render_to_string('email_verification.html', {
        'user': user,
        'activate_url': activate_url
    })

    email_msg = EmailMessage(subject, message, to=[email])
    email_msg.content_subtype = 'html'
    email_msg.send()

    return Response({'detail': '📩 인증 메일을 전송했습니다.'}, status=200)



# accounts/views.py
@api_view(['POST'])
@permission_classes([AllowAny])
def final_signup(request):
    uidb64 = request.data.get('uidb64')
    token = request.data.get('token')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'error': '유효하지 않은 사용자입니다.'}, status=400)

    if not token_generator.check_token(user, token):
        return Response({'error': '유효하지 않거나 만료된 토큰입니다.'}, status=400)

    user.is_active = True
    user.save()
    return Response({'message': '이메일 인증 성공'}, status=200)
