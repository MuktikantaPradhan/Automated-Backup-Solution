import os
import time
import shutil
import paramiko
import boto3

def backup_local_to_remote(local_path, remote_path, host, username, password):
   
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)

    
    stdin, stdout, stderr = ssh.exec_command(f"mkdir -p {os.path.dirname(remote_path)}")
    if stdout.channel.recv_exit_status() != 0:
        print(f"Error creating remote directory: {stderr.read().decode()}")
        ssh.close()
        return False

    
    sftp = ssh.open_sftp()
    sftp.put_r(local_path, remote_path)
    sftp.close()

    
    ssh.close()

    return True

def backup_local_to_s3(local_path, bucket_name, region):
   
   
    s3 = boto3.client('s3', region_name=region)

    
    try:
        s3.upload_folder(local_path, bucket_name)
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        return False

    return True

def main():
   
    local_path = "/path/to/local/directory"
    remote_path = "/path/to/remote/directory"
    host = "example.com"
    username = "backupuser"
    password = "backuppassword"
    bucket_name = "my-backup-bucket"
    region = "us-west-2"

   
    success = False
    if backup_local_to_remote(local_path, remote_path, host, username, password):
        print("Backup to remote server successful.")
        success = True
    if backup_local_to_s3(local_path, bucket_name, region):
        print("Backup to S3 successful.")
        success = True

   
    if success:
        print("Backup completed successfully.")
    else:
        print("Backup failed.")

if __name__ == "__main__":
    main()