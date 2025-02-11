import os
import paramiko

def send_file(namelist: str):

    hostname = os.getenv("SSH_HOST")
    username = os.getenv("SSH_NAME")
    password = os.getenv("SSH_PASS")
    remote_file_path = os.getenv("REMOTE_PATH")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    sftp = client.open_sftp()
    with sftp.file(remote_file_path, 'w') as remote_f:
        remote_f.write(namelist)