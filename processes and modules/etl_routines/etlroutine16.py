import paramiko
from etltools import SnowFlakeToDF
import os
from datetimetools import Alternative_date_variables
from plconfig import SecInfo as sec

date = Alternative_date_variables().month_year
i=sec()

host = i.a_host
username = i.a_user
pk_file_path = i.apk_path

list=[
 [f'SELECT * FROM {i.a_product};',str(i.p1+'_product_'+date+'.csv')]
,[f'SELECT * FROM {i.a_stock};',str(i.p1+'_stock_'+date+'.csv')]
#,[f'SELECT * FROM {i.a_sellout};',str(i.p1+'_sellout_'+date+'.csv')]
,[f'SELECT * FROM {i.a_warehouse};',str(i.p1+'_warehouse.csv')]]

for query,path in list:
    data = SnowFlakeToDF(query)
    data.df_to_csv(path,False)
    
for query, path in list:

    file = os.path.basename(path)
    
    local_file_path = path
    remote_file_path = file

    pk = paramiko.Ed25519Key.from_private_key_file(pk_file_path) 
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname=host, port=22, username=username, pkey=pk)
        sftp = ssh.open_sftp()
        files = sftp.put(local_file_path, remote_file_path)
        print(sftp.listdir())
        sftp.close()
        ssh.close()  
    except Exception as e:
        print(e, ' - Exception Raised!')
    os.remove(local_file_path)
i=''