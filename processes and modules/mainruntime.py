# libraries/modules
import pyautogui
import pyperclip
import os
import shutil
from plconfig import MachineInfo
import time
from pytesseract import pytesseract
import time
from verifiers import process_registrant
from datetimetools import Timer
#from apitools import load_to_gsheets
from datetimetools import Alternative_date_variables
from etltools import FileTransformer
# preciso de uma lógica que limpe os downloads a cada extração
pyautogui.FAILSAFE = False

"""
    Serve estritamente para fins de:
        - Definir os passos para para execução das extrações do Metabase.
"""

path_to_tesseract = (
    #r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    r"C:\Users\vinicius.ribeiro_sou\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)

pytesseract.tesseract_cmd = path_to_tesseract
#x1, y1, x2, y2 = 80, 994, 175, 1012

target_area = "EB Visualization"
target_path = ""

class VisualGuide:
    
    def __init__(self, limit=5, target=None, type=None):
        
        self.mscreenshot_area = mx1, my1, mx2, my2 = 5, 443, 559, 786
        self.gscreenshot_area = gx1, gy1, gx2, gy2 = 506, 532, 559, 555
        self.target = target
        self.limit = limit
        if type == 'g':
            
            self.screenshot_area = self.gscreenshot_area
            
        else:
            
            self.screenshot_area = self.mscreenshot_area
        
    
    def match_my_area(self):

        start_time = time.time()

        while True:

            current_time = time.time()
            elapsed_time = current_time - start_time

            screenshot = pyautogui.screenshot(region=(self.screenshot_area))
            self.text = pytesseract.image_to_string(screenshot).strip()

            if len(self.text) > self.target:

                return True

            if elapsed_time > self.limit:
                
                return False

            time.sleep(0.1)
    
    def match_non_empty(self):

        start_time = time.time()

        while True:

            current_time = time.time()
            elapsed_time = current_time - start_time
            screenshot = pyautogui.screenshot(region=(self.screenshot_area))
            text = pytesseract.image_to_string(screenshot).strip()
        
            if text != self.target:

                return True

            if elapsed_time > self.limit:

                return False

            time.sleep(0.1)

def match_path(original_file, format, limit, gsheets=None):
    
    isgsheet = gsheets
    machine_info = MachineInfo()
    start_time = time.time()

    while True:

        current_time = time.time()
        elapsed_time = current_time - start_time
        sourceLoc = (
            r"C:/Users/" + machine_info.win_user_with_path_string + r"/Downloads/"
        )
        searchStr = original_file
        direc = os.listdir(sourceLoc)
        
        fileList = []
        
        for file in direc:
            if file.startswith(searchStr) and file.endswith(format):
                f = open(sourceLoc + file, "r")
                fileList.append(sourceLoc + file)
                f.close()

        filewpath = "".join(fileList)

        if filewpath != "":
            return filewpath

        if elapsed_time > limit:
            return False

        time.sleep(1) #0.1

class ProcessRunner:
    def __init__(self, element):

        self.timer = Timer()
        self.machine_info = MachineInfo()
        self.report = element
        self.name = self.report.name
        self.link = self.report.link
        self.limit_time = self.report.limit_time
        self.original_file = self.report.original_file_name
        self.destination_list = self.report.default_destination_path
        self.error = False
        self.origin = ""
        self.destination = ""
        self.timer.start_count()
        self.first_element = self.destination_list[0]
        _, self.file_format = os.path.splitext(self.first_element)
        
        class_name = type(self.report).__name__
        self.first_class_letter = class_name[0]
        
    def win_r(self, text="Chrome"):
        
        pyautogui.hotkey("win", "d")
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(2)
        pyperclip.copy(text)
        pyperclip.paste()
        pyautogui.hotkey("ctrl", "v", interval=0.15)
        pyautogui.sleep(2)
        pyautogui.hotkey("enter")

    def check_old_files(self):

        sourceLoc = (
            r"C:/Users/" + self.machine_info.win_user_with_path_string + r"/Downloads/"
        )
        
        searchStr = self.original_file
        direc = os.listdir(sourceLoc)

        fileList = []

        for file in direc:

            if file.startswith(searchStr) and file.endswith(self.file_format):
                f = open(sourceLoc + file, "r")
                fileList.append(sourceLoc + file)
                f.close()

        filewpath = "".join(fileList)

        try:
            os.remove(filewpath)

        except:
            pass
        
    def download_gsheets(self):
        
        time.sleep(2)
        
        screen = VisualGuide(self.limit_time,'','g')
        
        screen.match_non_empty()
        
        if screen.match_non_empty() == True:
            
            pyautogui.click(85, 184)  
            pyautogui.click(172, 488) 
                
            if self.file_format == '.tsv':
                
                pyautogui.click(481, 702) 
                
            elif self.file_format == '.csv':

                pyautogui.click(538, 653) 

            else:

                pyautogui.click(498, 491) 
                        
        else:

            self.error = True
    
    def set_link(self):
        
        pyautogui.sleep(3)
        pyperclip.copy(self.link)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.sleep(1)
        pyautogui.press("enter")
    
        pyautogui.sleep(5)

        try:
            pyautogui.getWindowsWithTitle("Chrome")[0].maximize()

        except:
            self.error = True
            print("ProcessRunner: Chrome window not found.")
            
    def download_metabase(self):
            
        pyautogui.sleep(7)
        pyautogui.click(881, 606)
        pyautogui.click(941, 614)
        pyautogui.click(944, 613)
        pyautogui.sleep(5)

        screen = VisualGuide(self.limit_time,8)
        screen.match_my_area()
        
        if not screen.match_my_area() == True:

            self.error = True

        else:

            pass

        pyautogui.click(1834, 1001)
        pyautogui.sleep(3)

        self.destination_list = [
            str(i) for i in self.destination_list
        ]  # list comprehension from winpath to string obj
        self.first_element = self.destination_list[0]
        format = self.first_element[-3:]

        if format == "csv":

            pyautogui.click(1572, 780)

        else:

            pyautogui.click(1599, 856)

    def find_file(self):
     
        self.destination_list = self.destination_list
        self.destination_list = [str(i) for i in self.destination_list]
        
        if self.first_class_letter == 'L':
            self.file_format = '.xlsx'
        else:
            pass
        
        self.origin = match_path(self.original_file, self.file_format, self.limit_time)

        if self.origin == False:

            self.error = True
            print("ProcessRunner: Empty origin.")

        else:

            self.error = False
            #self.send()

    def send(self):
        for each_path in self.destination_list:
            try:
                time.sleep(2)
                self.destination = each_path
                shutil.copy(self.origin, self.destination)
            except Exception as e:
                print("ProcessRunner: Error transfering: "+str(e))

    def close_browser(self):

        try:
            time.sleep(2)
            pyautogui.getWindowsWithTitle("Chrome")[0].close()
        except:
            pass

    def check_error(self):

        if self.error:
            self.timer.finish_count()
            errr1 = (
                "ProcessRunner: Error for "
                + self.name
                + f" in (Metabase Script). Execution time: {int(self.timer.minutes)} minutes and {int(self.timer.seconds)} seconds. Started at "
                + self.timer.start
                + " and finished at "
                + self.timer.finish
                + "."
            )
            process_registrant.register_error(errr1)

        else:
            self.timer.finish_count()
            finish_message = (
                "ProcessRunner: "
                + self.name
                + " extraction started at "
                + self.timer.start
                + " finished at "
                + self.timer.finish
                + f". Execution time: {int(self.timer.minutes)} minutes and {int(self.timer.seconds)} seconds."
            )
            process_registrant.register_info(finish_message)
            
    def download_locus(self):
        
        date = Alternative_date_variables()
        date = date.yesterday_slash_separated_mm_dd_yyyy
        date = str(date)
        
        time.sleep(15)
        pyautogui.click(1361, 527)
        time.sleep(4)
        pyautogui.click(1009, 675)
        time.sleep(4)
        pyautogui.click(1004, 738)
        time.sleep(16)
        pyautogui.click(1873, 308)
        time.sleep(1)
        pyautogui.click(1811, 365) 
        time.sleep(1) 
        pyautogui.click(1031, 507)  

        time.sleep(2) 
        pyautogui.click(804, 550)  
        pyautogui.hotkey('ctrl', 'a')  
        pyperclip.copy(date)
        pyperclip.paste()
        pyautogui.hotkey("ctrl", "v", interval=0.15)

        pyautogui.click(1098, 546)  
        pyautogui.hotkey('ctrl', 'a')  
        pyperclip.copy(date)
        pyperclip.paste()
        pyautogui.hotkey("ctrl", "v", interval=0.15)

        time.sleep(1)
        pyautogui.click(946, 746)  
        time.sleep(2)
        pyautogui.click(1132, 804)  
        time.sleep(20)
        pyautogui.click(1560, 927)  
        
    def download_playvox(self):
        
        time.sleep(2)
        pyautogui.click(967, 569)
        time.sleep(2)
        pyautogui.click(1758, 536)
        time.sleep(5)
        pyautogui.click(1680, 161)
        pyautogui.click(1384, 278)
        time.sleep(8)
        pyautogui.click(1680, 161)
        pyautogui.click(1384, 278)
        time.sleep(7)
        pyautogui.click(1654, 403)
            
    def download_zendesk(self):
        
        time.sleep(10)
        pyautogui.click(814,653)
        pyautogui.click(967, 569)
        pyautogui.click(933, 658)
        time.sleep(4)
        pyautogui.click(335, 73)
        pyautogui.hotkey('ctrl', 'a')  
        pyperclip.copy(self.link)
        pyperclip.paste()
        pyautogui.hotkey("ctrl", "v", interval=0.15)
        pyautogui.hotkey('enter')  
        time.sleep(8)
        pyautogui.click(1869,230)
        pyautogui.click(1728,425)
        time.sleep(2)
        pyautogui.click(750, 437)
        time.sleep(1)
        pyautogui.click(750, 437)
        time.sleep(1)
        pyautogui.click(751, 347)
        time.sleep(1)
        pyautogui.click(1132,870)

    def download_extranet(self):
        
        time.sleep(10)
        pyautogui.click(814,653)
        pyautogui.click(967, 569)
        pyautogui.click(933, 658)
        time.sleep(4)
        pyautogui.click(335, 73)
        pyautogui.hotkey('ctrl', 'a')  
        pyperclip.copy(self.link)
        pyperclip.paste()
        pyautogui.hotkey("ctrl", "v", interval=0.15)
        pyautogui.hotkey('enter')  
        time.sleep(8)
        pyautogui.click(1869,230)
        pyautogui.click(1728,425)
        time.sleep(2)
        pyautogui.click(750, 437)
        time.sleep(1)
        pyautogui.click(750, 437)
        time.sleep(1)
        pyautogui.click(751, 347)
        time.sleep(1) 
    

    def send_to_destination_transformed_csv(self):

        if not self.error:
            ft = FileTransformer()
            ft.xlsx_to_csv(self.origin,self.destination_list)
        else: 
            pass
        
    def process_sorting(self):
        
        self.process_runner=ProcessRunner(self.report)
        time.sleep(4)
        self.process_runner.close_browser()           
        self.process_runner.timer.start_count()
        self.process_runner.check_old_files()
        self.process_runner.win_r(str('Chrome'))
        self.process_runner.set_link()
        
        if self.process_runner.error == False and self.first_class_letter   == 'M':
            self.process_runner.download_metabase()
        elif self.process_runner.error == False and self.first_class_letter == 'A':
            pass
        elif self.process_runner.error == False and self.first_class_letter == 'G':
            self.process_runner.download_gsheets()
        elif self.process_runner.error == False and self.first_class_letter == 'P':
            self.process_runner.download_playvox()
        elif self.process_runner.error == False and self.first_class_letter == 'L':
            self.process_runner.download_locus()
        elif self.process_runner.error == False and self.first_class_letter == 'Z':
            self.process_runner.download_zendesk()
        elif self.process_runner.error == False and self.first_class_letter == 'E':
            self.process_runner.download_extranet()
        else:
            pass
        
        if self.process_runner.error == False:
            self.process_runner.find_file()
        
        if self.process_runner.error == False and self.first_class_letter == 'L':
            self.process_runner.send_to_destination_transformed_csv()
        elif self.process_runner.error == False and self.first_class_letter != 'L':
            self.process_runner.send()
            
        if self.process_runner.error == False:
            self.process_runner.close_browser()
            self.process_runner.check_old_files()
            
        self.process_runner.check_error()