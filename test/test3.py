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

# Replace with your target device's details
host = "192.168.0.104"  # Replace with the target device's IP address
username = "sampad"
password = "Heinstein848"
command = "ls"  # Replace with the command you want to execute

output, error = execute_remote_command(host, username, password, command)

if output:
    print("Command Output:")
    print(output)
if error:
    print("Command Error:")
    print(error)
