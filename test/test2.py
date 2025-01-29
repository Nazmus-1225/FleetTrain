import requests
import websocket
import json
import uuid

# Base URL of your JupyterLab server
  # Replace with your JupyterLab server URL
TOKEN = "0700684dfbad354f9104fbf1e7ca10f9fd85eaf0b8196f38"  # Replace with your JupyterLab API token
BASE_URL = "http://localhost:8888"
# Headers with authorization token
HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json",
}

# Step 1: Start a new kernel
def start_kernel():
    response = requests.post(f"{BASE_URL}/api/kernels", headers=HEADERS)
    response.raise_for_status()
    return response.json()["id"]

# Step 2: Execute code
def execute_code(kernel_id, code):
    ws_url = f"{BASE_URL.replace('http', 'ws')}/api/kernels/{kernel_id}/channels"
    ws = websocket.create_connection(ws_url, header=[f"Authorization: Token {TOKEN}"])
    
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
    while True:
        msg = json.loads(ws.recv())
        #print(msg)
        if(msg['msg_type']=="execute_result"):
            result = msg["content"]["data"]["text/plain"]
            print(f"Execution Result: {result}")
            break
        

    ws.close()


# Step 3: Main function to run everything
def main():
    try:
        # Start a new kernel
        kernel_id = start_kernel()
        print(f"Kernel started with ID: {kernel_id}")
        csv_file_path="/home/sakib/Documents/FleetTrain/client_1.csv"
        # Execute code
        code1 = f"import pandas as pd\ndf = pd.read_csv('{csv_file_path}')\ndf.head(3)"
        code2 = f"df.tail(3)"
        execute_code(kernel_id, code1)
        execute_code(kernel_id, code2)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
