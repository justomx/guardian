import pandas as pd
import os
import shutil
from verifiers import process_registrant
import gspread 
import gspread_dataframe as gd
from oauth2client.service_account import ServiceAccountCredentials

class FileTransformer:
    
    def __init__(self):
        self.excel = None
        self.csv = None
    
    def xlsx_to_csv(self, origin, destination):

        self.excel = origin
        filename, extension = os.path.splitext(origin)
        self.csv   = filename + '.csv'
        self.destination_list = destination
        
        try:
            df = pd.read_excel(self.excel)
            df.to_csv(self.csv, index=False)
            for each in self.destination_list:
                shutil.copy(self.csv,each)
            os.remove(self.excel)
            return True
        
        except Exception as e:
            print('FileTransformer: '+str(e))
            return False

class GSheetDataLoader:

    def __init__(self,key,sheet):
        self.data = None
        self.name = None
        self.key = key
        self.sheet = sheet
        self.service_account = r'G:\Meu Drive\API KEYS\Google Cloud\titanium-cacao-363112-81ea07cec0ec.json'

    def load_to_gsheets(self):
        SCOPES = ['https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/drive',]

        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.service_account,SCOPES)

        gc = gspread.authorize(credentials)

        wks = gc.open_by_key(self.key)
        
        worksheet = wks.worksheet(self.sheet)
            
        worksheet.clear()
        
        worksheet.update('A1', 'data')

        v = [e[0:1] for e in worksheet.get_all_values()] 

        updated = self.data

        gd.set_with_dataframe(worksheet, updated)

        process_registrant.register_info(f"""load_to_gsheets from GSheetDataLoader: {self.name} data was successfully loaded to Google Sheet.""")

class FileToGSheets(GSheetDataLoader):

    def __init__(self,element,key,sheet,drop_duplicates=False): 
            super().__init__(key,sheet) # Initiating common attributes on the superclass by instantiating the superclass
            self.report = element
            self.name = self.report.name
            self.path = self.report.default_destination_path[0]
            _, self.format = os.path.splitext(self.path)
            self.duplicates_elimination = drop_duplicates

    def read_file(self):
        if self.format == '.csv':
            try:
                self.data = pd.read_csv(self.path,sep=',')
                return self.data

            except Exception as e:
                return process_registrant.register_error(f'read_file method from GSheetDataLoader: : {e}') 

        else:
            try:
                self.data = pd.read_excel(self.path)
                return self.data

            except Exception as e:
                return process_registrant.register_error(f'read_file method from GSheetDataLoader: : {e}') 
            
    def prepare_data(self):
        if self.duplicates_elimination:
            self.data.drop_duplicates(inplace=True)

    def force_load(self):
        self.read_file()
        self.prepare_data()
        self.load_to_gsheets()


class PhatomReport:

    def __init__(self,name,path):
        self.name = name
        self.default_destination_path = [path]