from reports import EReport01,EReport02
from etltools import load_to_gsheets
import os
from verifiers import send_message

# Google Sheets data load - Cupom All

keysd      = '1F-BgBPVjqcA4ml3Xdzpo8ZXkrnUT6Yxb0o1K4Tji1bw'
keynm      = '11Wmn2c94zY8iTDNXCt_cEcYXpGh-yEH8CohBQNwNaXQ'
prodi1 =[EReport01().name,EReport01().default_destination_path[0],os.path.splitext(EReport01().default_destination_path[0])[1],'SD',keysd,True]
prodi2 =[EReport02().name,EReport02().default_destination_path[0],os.path.splitext(EReport02().default_destination_path[0])[1],'NM',keynm,True]

cupon_list = [prodi1,prodi2] 
for each in cupon_list:
    try:
        load_to_gsheets(str(each[1]), str(each[2]), str(each[4]),str(each[3]),each[4])
    except Exception as e:
        e7='Error transfering data to sheets on the report <!channel>: '+str(each[0]+'. More details: '+str(e))
        print(e7)
        send_message(e7,'bot_channel')