import uuid
import requests
import websocket
from resources.models import Resource, Kernel
from .models import Notebook, NotebookLocations
import random
from decouple import config
import os
import json
import requests

def createNotebookFiles(id, num_of_nodes):
    notebook=Notebook.objects.get(id=id)
    directory = config('DIRECTORY')

    notebook_path = os.path.join(directory, f"{notebook.name}.ipynb")

    notebookLocation=NotebookLocations(
                notebook=notebook, location=notebook_path
            )
    notebookLocation.save()
    notebook_content = {
        "cells": [],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 4
    }

    with open(notebook_path, "w") as notebook_file:
        json.dump(notebook_content, notebook_file)
    if num_of_nodes>1:
        for i in range(0,num_of_nodes):
            notebook_path = os.path.join(directory, f"{notebook.name}_r{i}.ipynb")
            with open(notebook_path, "w") as notebook_file:
                json.dump(notebook_content, notebook_file)
            notebookLocation=NotebookLocations(
                notebook=notebook, location=notebook_path
            )
            notebookLocation.save()






def allocateResources(id, num_of_nodes):
    
    notebook=Notebook.objects.get(id=id)
    if num_of_nodes==1:
        n=num_of_nodes
    else:
        n=num_of_nodes+1
    resources = Resource.objects.filter(available__gt=0)

    type='central'
    for j in range (0,n):
        if(j>0):
            type='distributed'
        i=random.randint(0,len(resources)-1)
        resources[i].available-=1
        resources[i].used+=1
        resources[i].save()
        url=f"http://{resources[i].ip_address}:8888"
        HEADERS = {
            "Authorization": f"Token {resources[i].token}",
            "Content-Type": "application/json",
            }
        response = requests.post(f"{url}/api/kernels", headers=HEADERS)
        response.raise_for_status()
        kernel_id = response.json()["id"]
        kernel = Kernel(
            kernel_name=kernel_id,
            resource=resources[i],
            notebook=notebook,
            type=type
        )
        kernel.save()
        kernel_directory = f"/home/{resources[i].username}/fleettrain_files"
        command=f"mkdir -p {kernel_directory}/{kernel.id}"
        execute_remote_command(resources[i].ip_address, resources[i].username, resources[i].password, command)
        code = f"""
            import os
            os.chdir('{kernel_directory}/{kernel.id}')
            print('Current working directory:', os.getcwd())
        """
        execute_code(kernel.id,code)


import paramiko

def execute_remote_command(host, username, password, command):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add host keys

        # Connect to the remote host
        ssh.connect(hostname=host, username=username, password=password)

        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)

        # Read command output and errors
        output = stdout.read().decode()
        error = stderr.read().decode()

        # Close the connection
        ssh.close()

        return output, error
    except Exception as e:
        return None, str(e)

        
def execute_code(kernel_id, code):
    kernel = Kernel.objects.get(id=kernel_id)
    resource = kernel.resource
    ws_url = f"ws://{resource.ip_address}:8888/api/kernels/{kernel.kernel_name}/channels"
    ws = websocket.create_connection(ws_url, header=[f"Authorization: Token {resource.token}"])
    
    # Unique ID for the message
    msg_id = str(uuid.uuid4())
    # Message to execute code
    execute_msg = {
        "header": {
            "msg_id": msg_id,
            "username": "",
            "session": "",
            "msg_type": "execute_request",
            "version": "5.3",
        },
        "parent_header": {},
        "metadata": {},
        "content": {
            "code": code,
            "silent": False,
            "store_history": True,
            "user_expressions": {},
            "allow_stdin": True,
        },
        "channel": "shell"  # Specify the channel explicitly
    }
    
    ws.send(json.dumps(execute_msg))

    # Wait for response
    output = []
    while True:
        msg = json.loads(ws.recv())
        msg_type = msg['header']['msg_type']
        flag=0
        if msg_type == 'execute_result':
            output.append(msg['content']['data'].get('text/plain', ''))
            flag+=1
        elif msg_type == 'stream':
            output.append(msg['content']['text'])
            flag+=1
        elif msg_type == 'error':
            output.append(msg['content']['traceback'])
            flag=1
        if (flag>0):
            break
                
        # if msg_type == 'status' and msg['content']['execution_state'] == 'idle':
        #     break
    ws.close()
    return output



def deleteNotebookFiles(id, num_of_nodes):
    notebook=Notebook.objects.get(id=id)
    directory = config('DIRECTORY')

    notebook_path = os.path.join(directory, f"{notebook.name}.ipynb")
    print(notebook_path)
    os.remove(notebook_path)

    if num_of_nodes>1:
        for i in range(0,num_of_nodes):
            notebook_path = os.path.join(directory, f"{notebook.name}_r{i}.ipynb")
            os.remove(notebook_path)

def unallocateResources(id):
    notebook=Notebook.objects.get(id=id)
    kernels = Kernel.objects.filter(notebook=notebook)
    if kernels.exists():
        for kernel in kernels:
            try:
                resource_id = kernel.resource.id
                resource = Resource.objects.get(id=resource_id)
                resource.available+=1
                resource.used-=1
                resource.save()
                kernel_directory = f"/home/{resource.username}/fleettrain_files"
                command=f"rm -rf {kernel_directory}/{kernel.id}"
                execute_remote_command(resource.ip_address, resource.username, resource.password, command)
                
                kernel.delete()
            except Exception as e:
                print(f"Unexpected error while unallocating kernel {kernel.id}: {e}")

from scp import SCPClient


def save_to_remote_via_scp(file_path, remote_path, remote_host, username, password):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_host, username=username, password=password)

    with SCPClient(ssh.get_transport()) as scp:
        scp.put(file_path, remote_path)

def fetch_from_remote_via_ftp(remote_path, remote_host, username, password, local_path):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_host, username=username, password=password)

    sftp = ssh.open_sftp()

    # Download the file
    sftp.get(remote_path, local_path)
    print(f"File downloaded successfully to {local_path}")

    # Close connections
    sftp.close()
    ssh.close()