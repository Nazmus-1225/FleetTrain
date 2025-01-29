import os
import json
import uuid
from jupyter_client import KernelManager

# Central directory setup
CENTRAL_DIR = "/home/sakib/Documents/FleetTrain/Central_Directory"


# Function to create a new notebook and its folder
def create_notebook(notebook_name):
    notebook_id = str(uuid.uuid4())
    notebook_folder = os.path.join(CENTRAL_DIR, notebook_id)
    os.makedirs(notebook_folder, exist_ok=True)

    notebook_path = os.path.join(notebook_folder, f"{notebook_name}.ipynb")
    notebook_content = {
        "cells": [],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 4
    }

    with open(notebook_path, "w") as notebook_file:
        json.dump(notebook_content, notebook_file)

    print(f"Notebook created: {notebook_path}")
    return notebook_path, notebook_folder


# Function to upload dataset to the designated folder
def upload_dataset(notebook_folder, dataset_file_path):
    if not os.path.exists(dataset_file_path):
        raise FileNotFoundError(f"Dataset file not found: {dataset_file_path}")

    dataset_name = os.path.basename(dataset_file_path)
    dataset_dest_path = os.path.join(notebook_folder, dataset_name)

    with open(dataset_file_path, "r") as src_file, open(dataset_dest_path, "w") as dest_file:
        dest_file.write(src_file.read())

    print(f"Dataset uploaded: {dataset_dest_path}")
    return dataset_dest_path


# Function to execute code in a Jupyter kernel
def execute_code(notebook_path, code):
    km = KernelManager(kernel_name="python3")
    km.start_kernel()
    kc = km.client()
    kc.start_channels()

    try:
        # Execute the code
        msg_id = kc.execute(code)
        reply = kc.get_shell_msg(timeout=10)

        if reply["content"]["status"] == "ok":
            print(f"Code executed successfully.")
            print(reply)

        # Add a cell to the notebook
        with open(notebook_path, "r") as notebook_file:
            notebook_content = json.load(notebook_file)

        notebook_content["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": code.splitlines()
        })

        # Save the updated notebook
        with open(notebook_path, "w") as notebook_file:
            json.dump(notebook_content, notebook_file)

        print(f"Notebook updated and saved: {notebook_path}")

    finally:
        kc.stop_channels()
        km.shutdown_kernel()


# Example usage
if __name__ == "__main__":
    # Step 1: Create a notebook
    notebook_path, notebook_folder = create_notebook("example_notebook")

    # Step 2: Upload a dataset
    dataset_path = upload_dataset(notebook_folder, "/home/sakib/Documents/FleetTrain/client_1.csv")
    csv_file_path="/home/sakib/Documents/FleetTrain/client_1.csv"

    # Step 3: Execute code and update the notebook
    execute_code(notebook_path, f"import pandas as pd\ndf = pd.read_csv('{csv_file_path}')\ndf.head(3)")
