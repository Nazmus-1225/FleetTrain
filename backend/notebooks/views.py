# views.py
from django.http import FileResponse, JsonResponse
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
import json, os
from jupyter_client import KernelManager
from resources.models import Resource, Kernel
import uuid
from .models import Notebook,  NotebookLocations
from accounts.models import User
from .serializers import NotebookSerializer
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from decouple import config
import zipfile
from .utils import createNotebookFiles, allocateResources, deleteNotebookFiles, unallocateResources, save_to_remote_via_scp, execute_code, fetch_from_remote_via_ftp
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

import pandas as pd  
import numpy as np 
class DatasetUploadView(APIView):
    def post(self, request):
        if request.FILES.get('file'):
            notebook_id = request.POST.get('notebook_id')
            notebook=Notebook.objects.get(id=notebook_id)
            kernels=Kernel.objects.filter(notebook=notebook,type='central')
            resource=kernels[0].resource
            directory=config('DATASET_DIRECTORY')
            file = request.FILES['file']
            fs = FileSystemStorage(location=directory)
            filename = fs.save(file.name, file)
            kernel_directory = f"/home/{resource.username}/fleettrain_files"
            save_to_remote_via_scp(f"{directory}/{filename}",f"{kernel_directory}/{kernels[0].id}",resource.ip_address,resource.username,resource.password)
            if (notebook.type=='distributed'):
                df=pd.read_csv(f"{directory}/{filename}")
                shuffled_df = df.sample(frac=1, random_state=42).reset_index(drop=True)
                splits = np.array_split(shuffled_df, notebook.num_of_nodes)
                kernels=Kernel.objects.filter(notebook=notebook,type='distributed')
                for i, part in enumerate(splits):
                    filename = f"{directory}/temp/{file.name}"
                    part.to_csv(filename, index=False)
                    kernel=kernels[i]
                    resource=kernel.resource
                    kernel_directory = f"/home/{resource.username}/fleettrain_files"
                    save_to_remote_via_scp(f"{directory}/temp/{file.name}",f"{kernel_directory}/{kernel.id}",resource.ip_address,resource.username,resource.password)
                    print(f"Saved: {filename}")
            if os.path.exists(directory) and os.path.isdir(directory):
                for file in os.listdir(directory):  # Iterate over all files and subdirectories
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):  # Only delete files, not subdirectories
                        os.remove(file_path)
            directory=f"{directory}/temp"
            if os.path.exists(directory) and os.path.isdir(directory):
                for file in os.listdir(directory):  # Iterate over all files and subdirectories
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):  # Only delete files, not subdirectories
                        os.remove(file_path)
                
            return Response(status=status.HTTP_200_OK)


class FetchFilesView(APIView):
    def get(self, request, pk):
            notebook=Notebook.objects.get(id=pk)
            kernel=Kernel.objects.filter(notebook=notebook,type='central').first()
            output=(execute_code(kernel.id,"!ls"))
            string_value = output[0].strip()
            file_list = string_value.split()
            return Response(file_list,status=status.HTTP_200_OK)
    
class DownloadNotebooksView(APIView):
    def get(self, request, pk):
            notebook=Notebook.objects.get(id=pk)
            notebookLocations=NotebookLocations.objects.filter(notebook=notebook)
            zip_filename = f"{notebook.name}.zip"
            zip_path = os.path.join(config('DOWNLOAD_DIRECTORY'), zip_filename)
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for notebookLocation in notebookLocations:
                    file_path=notebookLocation.location
                    if os.path.exists(file_path):
                        zipf.write(file_path, os.path.basename(file_path))

            return FileResponse(open(zip_path, 'rb'), as_attachment=True, filename=zip_filename)
    
class DownloadFilesView(APIView):
    def get(self, request, pk, filename):
            notebook=Notebook.objects.get(id=pk)
            kernel=Kernel.objects.filter(notebook=notebook,type='central').first()
            resource=kernel.resource
            file_path=f"/home/{resource.username}/fleettrain_files/{kernel.id}/{filename}"
            fetch_from_remote_via_ftp(file_path,resource.ip_address,resource.username,resource.password,f"{config('DOWNLOAD_DIRECTORY')}/{filename}")
            final_path=f"{config('DOWNLOAD_DIRECTORY')}/{filename}"
            return FileResponse(open(final_path, 'rb'), as_attachment=True, filename=filename)

import re
class ExecuteCodeView(APIView):
    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        #print(json.dumps(data, indent=4))
        cells=data['cells']
        code=data['code']
        type=data['type']
        notebook_id=data['notebook_id']
        
        notebook=Notebook.objects.get(id=notebook_id)
        
        if(type=='central'):
            notebookLocations=NotebookLocations.objects.filter(notebook=notebook,location__endswith=f"{notebook.name}.ipynb")
            kernels=Kernel.objects.filter(notebook=notebook,type='central')
        if(type=='distributed'):
            notebookLocations=[]
            for i in range(0,notebook.num_of_nodes):
                notebookLocation=NotebookLocations.objects.filter(notebook=notebook,location__endswith=f"{notebook.name}_r{i}.ipynb").first()
                notebookLocations.append(notebookLocation)
                kernels=Kernel.objects.filter(notebook=notebook,type='distributed')
                pattern = r'(\w+)\.(train|fit)\('
                matches = re.findall(pattern, code)
                if(len(matches)>0):
                    variables = [match[0] for match in matches]
                    print(variables[0])
        outputs=[]
        for i,kernel in enumerate(kernels):
            print(i)
            output=execute_code(kernel.id,code)
            outputs.append(output)
            written=[]
            for cell in cells:
                if(cell['code']==code):
                    print(i)
                    cell['outputs'][i]=output
                written.append(cell)
            notebook_content = {
            "cells": written,
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 4
            }
            with open(notebookLocations[i].location, "w") as notebook_file:
                json.dump(notebook_content, notebook_file)
        return Response(outputs, status=status.HTTP_200_OK)
    
class FetchNotebookView(APIView):
    def get(self,request,pk):
        cells=request.POST.get('cells')
        code=request.POST.get('code')
        type=request.POST.get('type')
        notebook_id=request.POST.get('id')
        notebook=Notebook.objects.get(id=notebook_id)
        notebookLocations=NotebookLocations.objects.filter(notebook=notebook)
        if(type=='central'):
            notebookLocations=NotebookLocations.objects.filter(notebook=notebook,location__endswith=f"{notebook.name}.ipynb")
            kernels=Kernel.objects.filter(notebook=notebook,type='central')
        if(type=='distributed'):
            for i in range(0,notebook.num_of_nodes):
                notebookLocations=NotebookLocations.objects.filter(notebook=notebook,location__endswith=f"r{i}.ipynb")
                kernels=Kernel.objects.filter(notebook=notebook,type='distributed')
        outputs=[]
        for i,kernel in enumerate(kernels):
            output=execute_code(kernel.id,code)
            outputs.append(output)
            written=[]
            for cell in cells:
                if(cell['code']==code):
                    cell['outputs'][i]=output
                written.append(cell)
            notebook_content = {
            "cells": written,
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 4
            }
            with open(notebookLocations[i].location, "w") as notebook_file:
                json.dump(notebook_content, notebook_file)
        return Response(outputs, status=status.HTTP_200_OK)
