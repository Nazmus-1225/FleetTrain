# accounts/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer, LoginSerializer
from .utils import create_jwt, decode_jwt
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BaseAuthentication

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            user_id = decode_jwt(token)
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    return (user, token)
                except User.DoesNotExist:
                    pass
        return None

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            token = create_jwt(user.id)
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyTokenView(APIView):
    

    def get(self, request):
        return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)
