from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
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
