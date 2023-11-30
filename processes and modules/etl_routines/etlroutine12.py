import pyodbc
import pandas as pd
from plconfig import MachineInfo as machine_info,SecInfo as sec
import os
from azure.storage.blob import BlobServiceClient
from verifiers import send_message
from etltools import PhatomReport,FileToGSheets
 
pss = sec().snf_pss

conn_str = f"DSN=Snowflake;UID=VINICIUS_RIBEIRO;PWD={pss};"
conn = pyodbc.connect(conn_str)

query = """
SELECT * 

FROM BR_JUSTO_PROD.SANDBOX.PLACED_SALES_BY_CLUSTER

;
"""

df = pd.read_sql(query, conn)

file = str(r'G:'+machine_info().pathlang0+r'\Data & Performance\Relatórios de Growth\0 - ECOMMERCE\order_history_new\gmvp_by_day.csv')
df.to_csv(file,index=False)

conn.close()

placed_data_allbases_report = PhatomReport('Base LG',file)
placed_data_load = FileToGSheets(placed_data_allbases_report,'1QBPcfxqucGalXPUYtetpACbspa58DN1rcaYRVqZHW1Q','Placed',True)
placed_data_load.force_load()