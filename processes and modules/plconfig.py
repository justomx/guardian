import locale
import ctypes
import os
import glob
from pathlib import Path

"""
    Serve estritamente para fins de:
        - Armazenar configurações de acessos, linguagem, caminhos e funções.
"""

# Last Mile Folders Cleaner

class FolderUpperCleaner:

    def __init__(self):
        self.process = []
        self.process_name =""

    def delete(self,files_list):
        try:
            for f in files_list:
                os.remove(f)
        except:
            print('FolderUpperCleaner: None to be remove for '+self.process_name+'.')

    def last_mile_set(self):

        machine_info=MachineInfo()

        dir=[r'G:'+machine_info.pathlang0+r'/Data & Performance/Relatórios Last Mile/Novo Mundo/0 - AVANCO DO DIA POR ARMAZEM/*'
            ,r'G:'+machine_info.pathlang0+r'/Data & Performance/Relatórios Last Mile/Novo Mundo/1 - CLOSED DELIVERED BY WAREHOUSE/*'
            ,r'G:'+machine_info.pathlang0+r'/Data & Performance/Relatórios Last Mile/Novo Mundo/2 - LINHAS PARA PICKEAR ARMAZEM SEPARADO POR PASILLO/*'
            ,r'G:'+machine_info.pathlang0+r'/Data & Performance/Relatórios Last Mile/0 - AVANCO DO DIA POR ARMAZEM/*'
            ,r'G:'+machine_info.pathlang0+r'/Data & Performance/Relatórios Last Mile/1 - CLOSED DELIVERED BY WAREHOUSE/*'
            ,r'G:'+machine_info.pathlang0+r'/Data & Performance/Relatórios Last Mile/2 - LINHAS PARA PICKEAR ARMAZEM SEPARADO POR PASILLO/*']
        try:          
            for each in dir:
                files = glob.glob(each)
                self.delete(files)   
        except:
            print('FolderUpperCleaner: Not possible to insert the list of files in the delete method.')

    def clean_downloads(self):

        dir = r'C:/Users/Justo Dashboard/Downloads/*'
        
        try:            

            files = glob.glob(dir)
            self.delete(files)

        except Exception as e:
            print('FolderUpperCleaner: Not possible to insert the list of files in the delete method (Dowloads Folder).')
            print(f"Caught an exception: "+str(e))

    def remove_call(self, process_name):
        self.process_name = process_name
        if process_name == 'lastmile':
            self.last_mile_set()
        else:
            print('FolderUpperCleaner: Argument unknown')

# Pc info

class MachineInfo():

    def __init__(self):
        self.windll = ctypes.windll.kernel32
        self.remote_repo_ip ='11.11.10.7'
        self.win_user= os.getlogin( )
        self.win_user_with_path_string = r'\\'+ self.win_user
        self.lang = locale.windows_locale[self.windll.GetUserDefaultUILanguage() ]
        if self.lang == 'pt_BR':
            self.pathlang0     ='\Drives compartilhados'
            self.pathlang1     ='\Meu Drive'
            self.pathlang2     ='/Drives compartilhados'
            self.pathlang3     ='/Meu Drive'
        if self.lang == 'en_US':
            self.pathlang0     ='\Shared drives'
            self.pathlang1     ='\My Drive'
            self.pathlang2     ='/Shared drives'
            self.pathlang3     ='/My Drive'

# Secrets

class SecInfo:

    def __init__(self):
        self.config = self._read_secret('G:'+MachineInfo().pathlang1+'\API KEYS\Secrets\9eYRqXm6eZTfu6P3hsRdWw.txt')
        self.sas_url_unilever = self.config.get('UNILEVER_BLOB_ADDRESS_TO_CODE')
        self.sas_url_ambev    = self.config.get('AMBEV_BLOB_ADDRESS_TO_CODE')
        self.snf_pss          = self.config.get('SNF_PSS')

    def _read_secret(self, filepath):
        try:
            config = {}
            with open(filepath, 'r') as sec_file:
                for line in sec_file:
                    parts = line.strip().split('=')
                    key = parts[0]
                    value = '='.join(parts[1:])
                    config[key] = value
            return config
        except FileNotFoundError:
            print("File with secret no found.")
            return {}
        except KeyError as e:
            print(f"Key not found in the file: {e}")
            return {}
        
machine_info = MachineInfo()