# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
import json
from jupyter_client import KernelManager
import uuid
from .models import Notebook
from .serializers import NotebookSerializer
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

# Store kernel managers for each notebook
notebook_kernels = {}

@csrf_exempt
@require_http_methods(["POST"])
def create_notebook(request):
    notebook_id = str(uuid.uuid4())
    
    # Initialize a kernel for this notebook
    km = KernelManager()
    km.start_kernel()
    
    notebook_kernels[notebook_id] = {
        'kernel_manager': km,
        'kernel_client': km.client()
    }
    
    return JsonResponse({
        'notebook_id': notebook_id
    })

@csrf_exempt
@require_http_methods(["POST"])
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

@csrf_exempt
@require_http_methods(["POST"])
def save_notebook(request, notebook_id):
    try:
        data = json.loads(request.body)
        cells = data.get('cells', [])
        
        # Here you would implement notebook saving logic
        # You might want to save to a database or file system
        
        return JsonResponse({
            'message': 'Notebook saved successfully'
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
                if(notebook.user_id==decoded_token['id']):
                    notebook.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)