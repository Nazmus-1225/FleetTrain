# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import jupyterlab
from jupyter_client import KernelManager
import uuid

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