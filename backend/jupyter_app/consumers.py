from channels.generic.websocket import AsyncWebsocketConsumer
import json
from kernel_manager import NotebookKernelManager

class NotebookConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.notebook_id = self.scope['url_route']['kwargs']['notebook_id']
        await self.channel_layer.group_add(
            f"notebook_{self.notebook_id}",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"notebook_{self.notebook_id}",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        code = data['code']
        
        # Execute code and send back results
        kernel_manager = NotebookKernelManager()
        outputs = kernel_manager.execute_code(self.notebook_id, code)
        
        await self.send(text_data=json.dumps({
            'outputs': outputs
        }))