# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
import json, os
from jupyter_client import KernelManager
import uuid
from .models import Notebook, Cell, NotebookLocations
from accounts.models import User
from .serializers import NotebookSerializer
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from decouple import config
from .utils import createNotebookFiles, allocateResources, deleteNotebookFiles, unallocateResources
class NotebookCreateView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', None)
        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if decoded_token["role"]=="user":
                type=request.data.get('type')
                nodes=request.data.get('nodes')
                user_id=User(id=decoded_token['id'])
                notebook=Notebook(
                    user_id=user_id,
                    type=type,
                    num_of_nodes=nodes
                )
                
                notebook.save()
                name=f"Notebook_{notebook.id}"
                notebook.name=name
                notebook.save()
                return Response({"notebook_id":notebook.id},status=status.HTTP_200_OK)
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

class NotebookOpenView(APIView):
    def get(self, request, pk):
        token = request.headers.get('Authorization', None)
        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if decoded_token["role"]=="user":
                notebook = Notebook.objects.get(id=pk)
                serializer=NotebookSerializer(notebook)
                user_id=User(id=decoded_token['id'])
                if(notebook.user_id==user_id):
                    notebook_locations = NotebookLocations.objects.filter(notebook=notebook)
                    if(len(notebook_locations)==0):
                        createNotebookFiles(notebook.id,notebook.num_of_nodes)
                    allocateResources(notebook.id,notebook.num_of_nodes)
                    return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        
class NotebookCloseView(APIView):
    def delete(self, request, pk):
        unallocateResources(pk)
        return Response(status=status.HTTP_200_OK)



def execute_code(request, notebook_id):
    try:
        data = json.loads(request.body)
        code = data.get('code')
        cell_id = data.get('cell_id')
        
        if notebook_id not in notebook_kernels:
            return JsonResponse({
                'error': 'Notebook not found'
            }, status=404)
        
        kernel_client = notebook_kernels[notebook_id]['kernel_client']
        
        # Execute code
        msg_id = kernel_client.execute(code)
        
        # Get the output
        output = []
        while True:
            try:
                msg = kernel_client.get_iopub_msg(timeout=10)
                msg_type = msg['header']['msg_type']
                
                if msg_type == 'execute_result':
                    output.append(msg['content']['data'].get('text/plain', ''))
                elif msg_type == 'stream':
                    output.append(msg['content']['text'])
                elif msg_type == 'error':
                    return JsonResponse({
                        'error': '\n'.join(msg['content']['traceback'])
                    }, status=400)
                
                if msg_type == 'status' and msg['content']['execution_state'] == 'idle':
                    break
                    
            except Exception as e:
                return JsonResponse({
                    'error': str(e)
                }, status=500)
        
        return JsonResponse({
            'output': '\n'.join(output)
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


def cleanup_kernel(notebook_id):
    if notebook_id in notebook_kernels:
        try:
            notebook_kernels[notebook_id]['kernel_manager'].shutdown_kernel()
            del notebook_kernels[notebook_id]
        except Exception as e:
            print(f"Error cleaning up kernel: {e}")


class NotebookListView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', None)
        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if decoded_token["role"]=="user":
                notebooks = Notebook.objects.filter(user_id=decoded_token['id'])
                serializer = NotebookSerializer(notebooks, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        
class NotebookDeleteView(APIView):
    def delete(self, request, pk):
        token = request.headers.get('Authorization', None)
        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if decoded_token["role"]=="user":
                notebook = Notebook.objects.get(id=pk)
                user_id=User(id=decoded_token['id'])
                if(notebook.user_id==user_id):
                    deleteNotebookFiles(notebook.id,notebook.num_of_nodes)
                    notebook.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        
