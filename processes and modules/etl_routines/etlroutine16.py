import paramiko
from etltools import SnowFlakeToDF
import os
from datetime import datetime, timedelta
from plconfig import SecInfo as sec

 
current_year = datetime.today().year

i = sec()

host = i.a_host
username = i.a_user
pk_file_path = i.apk_path
 
for day in range(1, 32):
 
    july_date = datetime(current_year, 7, day)
    date_str = july_date.strftime("%Y-07-%d")
 
    queries_and_paths = [
        [f"SELECT * FROM {i.a_product};",                                f"{i.p1}_product_{date_str}.csv"],
        [f"SELECT * FROM {i.a_stock}   WHERE DATE = '{str(date_str)}';", f"{i.p1}_stock_{date_str}.csv"],
        [f"SELECT * FROM {i.a_sellout} WHERE DATE = '{str(date_str)}';", f"{i.p1}_sellout_{date_str}.csv"],
        [f"SELECT * FROM {i.a_sellin}  WHERE DATE = '{str(date_str)}';", f"{i.p1}_sellin_{date_str}.csv"],
        [f"SELECT * FROM {i.a_warehouse};",                              f"{i.p1}_warehouse_{date_str}.csv"]
        
    ]

    for query, path in queries_and_paths:
        data = SnowFlakeToDF(query)
        data.df_to_csv(path, index=False, separator=';')

    for query, path in queries_and_paths:
        file = os.path.basename(path)
        
        local_file_path = path
        remote_file_path = file

        pk = paramiko.Ed25519Key.from_private_key_file(pk_file_path) 
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(hostname=host, port=22, username=username, pkey=pk)
            sftp = ssh.open_sftp()
            sftp.put(local_file_path, remote_file_path)
            print(f'File uploaded: {remote_file_path}')
            sftp.close()
        except Exception as e:
            print(e, ' - Exception Raised!')
        finally:
            ssh.close()
            os.remove(local_file_path)
