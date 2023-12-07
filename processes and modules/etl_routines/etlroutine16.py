
#to install paramiko use pip install paramiko
import paramiko

# doc https://docs.paramiko.org/en/2.2/api/sftp.html

#Enable if you want log transaction
#paramiko_log = "paramiko.log"
#paramiko.util.log_to_file("paramiko_log")

#Must only use hostname and not http or https
host = "s-1cdbdac097ec48bfb.server.transfer.us-east-1.amazonaws.com"
        
#SFTP username
username = "user-justo"

#The private key file path, either use full file path or the file name is the file in the same folder of that script
private_key_file_path = 'C:/Users/vinicius.ribeiro_sou/.ssh/id_ed25519'

#local file path, either use full file path or the file name is the file in the same folder of that script
local_file_path = 'teste.txt'

#remote file path, either use full file path or the file name is the file in the same folder of that script
remote_file_path = 'teste.txt'

private_key = paramiko.Ed25519Key.from_private_key_file(private_key_file_path) 
  
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#Try/Catch, if connection fails, an exception will be raised
try:
    #Open SFTP Connection using paramiko SSHClient
    ssh.connect(hostname=host, port=22, username=username, pkey=private_key)
    sftp = ssh.open_sftp()
    #Execute a Put command that will upload a local file to a remote path in SFTP
    files = sftp.put(local_file_path, remote_file_path)
    print(sftp.listdir())
    #Closes SFTP and Connection
    sftp.close()
    ssh.close() 
except Exception as e:
    print(e, ' - Exception Raised!')