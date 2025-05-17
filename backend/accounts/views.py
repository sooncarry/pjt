from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer

@api_view(['POST'])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': '회원가입 성공'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
