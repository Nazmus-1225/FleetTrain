import os
import json
import requests

# JupyterLab server URL (replace with your server URL)
JUPYTERLAB_URL = "http://localhost:8888"  # Example URL

# Token for JupyterLab server authentication (if required)
API_TOKEN = "b3a23992c3adabf4f0c00c52640ab5fef3bf2dede1d2b47f"  # Replace with your Jupyter token

# Headers for API requests
HEADERS = {
    "Authorization": f"Token {API_TOKEN}",
    "Content-Type": "application/json",
}


# 0. Initialize Central Directory
def initialize_central_directory(directory="FleetTrain"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    print(f"Central directory initialized at: {directory}")
    return os.path.abspath(directory)


# 1. Create Notebook
def create_notebook(central_dir, notebook_name):
    notebook_path = os.path.join(central_dir, notebook_name + ".ipynb")
    dataset_folder = os.path.join(central_dir, notebook_name)

    # Create notebook
    notebook_content = {
        "cells": [],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    with open(notebook_path, "w") as f:
        json.dump(notebook_content, f)
    print(f"Notebook created: {notebook_path}")

    # Create dataset folder
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    print(f"Dataset folder created: {dataset_folder}")

    return notebook_path, dataset_folder


# 2. Upload Dataset to JupyterLab
def upload_dataset(notebook_folder, file_path):
    file_name = os.path.basename(file_path)
    destination_path = f"{notebook_folder}/{file_name}"

    # Read the file
    with open(file_path, "rb") as f:
        file_content = f.read()

    # Convert to base64 (required by JupyterLab API for binary files)
    file_content_base64 = file_content.decode("latin1")

    # Prepare the payload
    payload = {
        "type": "file",
        "format": "base64",
        "content": file_content_base64,
    }

    # Upload the file
    url = f"{JUPYTERLAB_URL}/api/contents/{destination_path}"
    response = requests.put(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        print(f"Dataset uploaded successfully: {destination_path}")
    else:
        print(f"Failed to upload dataset: {response.status_code} {response.text}")


# 3. Execute Code in Notebook
def execute_code(notebook_path, code):
    # Load the notebook
    with open(notebook_path, "r") as f:
        notebook_content = json.load(f)

    # Add a new code cell
    new_cell = {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": code}
    notebook_content["cells"].append(new_cell)

    # Save the notebook
    with open(notebook_path, "w") as f:
        json.dump(notebook_content, f)
    print(f"Code added to notebook: {code}")

    # Execute the notebook
    url = f"{JUPYTERLAB_URL}/api/kernels"
    data = {"notebook_path": notebook_path}
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Failed to execute code: {response.text}")


# Main function to demonstrate the workflow
def main():
    # Step 0: Initialize
    central_dir = initialize_central_directory()

    # Step 1: Create Notebook
    notebook_path, dataset_folder = create_notebook(central_dir, "example_notebook")

    # Step 2: Upload Dataset
    #upload_dataset(dataset_folder, "/home/sakib/Documents/FleetTrain/client_1.csv")  # Replace with your dataset file path

    # Step 3: Execute Code
    execute_code(notebook_path, "print('Hello, FleetTrain!')")


if __name__ == "__main__":
    main()
