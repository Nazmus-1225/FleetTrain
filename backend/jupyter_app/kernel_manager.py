from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager
import queue
import threading

class NotebookKernelManager:
    def __init__(self):
        self.kernel_managers = {}
        self.kernel_clients = {}
        
    def start_kernel(self, notebook_id):
        if notebook_id in self.kernel_managers:
            return
            
        km = KernelManager()
        km.start_kernel()
        
        kc = km.client()
        kc.start_channels()
        
        self.kernel_managers[notebook_id] = km
        self.kernel_clients[notebook_id] = kc
        
    def execute_code(self, notebook_id, code):
        if notebook_id not in self.kernel_clients:
            self.start_kernel(notebook_id)
            
        kc = self.kernel_clients[notebook_id]
        msg_id = kc.execute(code)
        
        # Collect the outputs
        outputs = []
        while True:
            try:
                msg = kc.get_iopub_msg(timeout=1)
                if msg['parent_header']['msg_id'] != msg_id:
                    continue
                
                msg_type = msg['header']['msg_type']
                content = msg['content']
                
                if msg_type == 'execute_result':
                    outputs.append({
                        'type': 'execute_result',
                        'data': content['data']
                    })
                elif msg_type == 'stream':
                    outputs.append({
                        'type': 'stream',
                        'name': content['name'],
                        'text': content['text']
                    })
                elif msg_type == 'error':
                    outputs.append({
                        'type': 'error',
                        'ename': content['ename'],
                        'evalue': content['evalue'],
                        'traceback': content['traceback']
                    })
                elif msg_type == 'status' and content['execution_state'] == 'idle':
                    break
            except queue.Empty:
                break
                
        return outputs