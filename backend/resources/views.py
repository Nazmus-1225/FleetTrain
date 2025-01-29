from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Resource, Kernel
from .serializers import ResourceSerializer, KernelSerializer
import jwt
from django.conf import settings

class ResourceListView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', None)
        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if decoded_token["role"]=="admin":
                resources = Resource.objects.all()
                serializer = ResourceSerializer(resources, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        
class ResourceCreateView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', None)
        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if decoded_token["role"]=="admin":
                ip_address = request.data.get('ip_address')
                max_kernels = request.data.get('max_kernels')
                res_token = request.data.get('token')
                username = request.data.get('username')
                password = request.data.get('password')
                if not ip_address or not max_kernels:
                    return Response({"error": "ip_address and max_kernels are required fields."}, status=status.HTTP_400_BAD_REQUEST)

                resource = Resource(
                    ip_address=ip_address,
                    max_kernels=int(max_kernels),  # Ensure it's converted to an integer
                    used=0,                        # Default value for 'used'
                    available=int(max_kernels),
                    token=res_token,
                    username=username,
                    password=password     # Initial available kernels
                )
                resource.save()
                serializer = ResourceSerializer(resource)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

class ResourceDeleteView(APIView):
    def delete(self, request, pk):
        token = request.headers.get('Authorization', None)
        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if decoded_token["role"]=="admin":
                resource = Resource.objects.get(id=pk)
                resource.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        

class KernelListView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', None)
        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if decoded_token["role"]=="admin":
                kernels = Kernel.objects.all()
                serializer = KernelSerializer(kernels, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

