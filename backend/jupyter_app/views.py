from django_restframework import viewsets, status, permissions, Response, action
from .models import Notebook
from .serializers import NotebookSerializer
from .kernel_manager import NotebookKernelManager
from django.shortcuts import get_object_or_404
import uuid 
class NotebookViewSet(viewsets.ModelViewSet):
    serializer_class = NotebookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Return only notebooks owned by the current user
        return Notebook.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        notebook = self.get_object()
        cell_id = request.data.get('cell_id')
        code = request.data.get('code')
        
        if not code:
            return Response(
                {'error': 'No code provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            kernel_manager = NotebookKernelManager()
            outputs = kernel_manager.execute_code(notebook.id, code)
            
            # Update the cell outputs in the notebook content
            notebook_content = notebook.content
            cells = notebook_content.get('cells', [])
            
            for cell in cells:
                if cell['id'] == cell_id:
                    cell['outputs'] = outputs
                    break
                    
            notebook.content = notebook_content
            notebook.save()
            
            return Response({
                'cell_id': cell_id,
                'outputs': outputs
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def add_cell(self, request, pk=None):
        notebook = self.get_object()
        cell_type = request.data.get('type', 'code')
        position = request.data.get('position', -1)
        
        if cell_type not in ['code', 'markdown']:
            return Response(
                {'error': 'Invalid cell type'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        new_cell = {
            'id': str(uuid.uuid4()),
            'type': cell_type,
            'content': '',
            'outputs': []
        }

        notebook_content = notebook.content
        cells = notebook_content.get('cells', [])
        
        if position == -1 or position >= len(cells):
            cells.append(new_cell)
        else:
            cells.insert(position, new_cell)
            
        notebook_content['cells'] = cells
        notebook.content = notebook_content
        notebook.save()
        
        return Response(new_cell)

    @action(detail=True, methods=['post'])
    def update_cell(self, request, pk=None):
        notebook = self.get_object()
        cell_id = request.data.get('cell_id')
        content = request.data.get('content')
        
        if not cell_id:
            return Response(
                {'error': 'No cell_id provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        notebook_content = notebook.content
        cells = notebook_content.get('cells', [])
        cell_updated = False
        
        for cell in cells:
            if cell['id'] == cell_id:
                cell['content'] = content
                cell_updated = True
                break
                
        if not cell_updated:
            return Response(
                {'error': 'Cell not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        notebook.content = notebook_content
        notebook.save()
        
        return Response({'status': 'cell updated'})

    @action(detail=True, methods=['post'])
    def delete_cell(self, request, pk=None):
        notebook = self.get_object()
        cell_id = request.data.get('cell_id')
        
        if not cell_id:
            return Response(
                {'error': 'No cell_id provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        notebook_content = notebook.content
        cells = notebook_content.get('cells', [])
        original_length = len(cells)
        
        cells = [cell for cell in cells if cell['id'] != cell_id]
        
        if len(cells) == original_length:
            return Response(
                {'error': 'Cell not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        notebook_content['cells'] = cells
        notebook.content = notebook_content
        notebook.save()
        
        return Response({'status': 'cell deleted'})