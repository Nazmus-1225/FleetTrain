from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import User
from .serializers import UserSerializer, LoginSerializer
import jwt
from django.conf import settings

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                if check_password(serializer.validated_data['password'], user.password):
                    # Generate JWT token
                    payload = {
                        'id': user.id,
                        'email': user.email,
                        'role': user.role
                    }
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                    
                    
                    return Response({
                        "token": token,
                        "role": user.role
                    }, status=status.HTTP_200_OK)
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JWTVerifyView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', None)
        if not token:
            return Response({"message": "Token not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            token = token.split(" ")[1]  # Remove "Bearer" if present
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return Response({"message": "JWT is valid!", "user": decoded_token}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
