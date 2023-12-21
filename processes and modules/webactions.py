from verifiers import process_registrant
from plconfig import SecInfo as sec 
from playwright.sync_api import sync_playwright 
import time
import json
from reports import MReport02 as rep
import pyperclip
import pyautogui

class BrowserInitiator:

    def __init__(self):
        self.browser=None
        self.context=None
        self.page=None
        self.cookies=sec()

    def start_browser(self,p): 
        self.browser = p.chromium.launch(headless=False)
        self.context = self.browser.new_context(accept_downloads=True)
        self.context.add_cookies(self.cookies)
        self.page = self.context.new_page()
        self.page.goto(self.link)
    
    def start_browser_new_context(self,p):  
        self.browser = p.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto(self.link)
        pyautogui.getWindowsWithTitle("Chromium")[0].maximize()

    def cookies_identifier(self):
        if self.__class__.__name__=='MetabaseExtractor':
            return self.cookies.mb_cookies
        elif self.__class__.__name__=='':
            pass
        elif self.__class__.__name__=='':
            pass

    def load_cookies(self):
        with open(self.cookies_identifier(),'r') as f:
            self.cookies = json.load(f)
            
    def close_browser(self):
        if self.browser:
            self.browser.close()

class Authenticator(BrowserInitiator):

    def __init__(self):
        super().__init__()
        self.link = sec()
        self.credentias = sec()

    def fill(self,value):
        time.sleep(10)
        pyperclip.copy(value)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")
        time.sleep(10)

    def authenticate_metabase(self):
        self.link = self.link.mb_url
        with sync_playwright() as p:
            self.start_browser_new_context(p) 
            login = '[class="AuthButtonstyled__CardText-j2pohn-3 gAbWId"]'
            self.page.wait_for_selector(login,timeout=(30*1000))  
            self.page.click(login)
            self.fill(self.credentias.xusr) 
            self.fill(self.credentias.xpss)
            cookies = self.context.cookies()
            with open(self.cookies.mb_cookies, 'w') as f:
                json.dump(cookies, f) 
            self.close_browser()

class MetabaseExtractor(BrowserInitiator):

    def __init__(self,time,link,path,format):
        super().__init__()
        self.time = time 
        self.link = link
        self.path = path
        self.format = format

    def extract_data(self):

        self.load_cookies() 

        with sync_playwright() as p: 

            self.start_browser(p)
            button = '[title="Download this data"]'
            self.page.wait_for_selector(button,timeout=(self.time*1000)) 
            self.page.click(button)  
            if self.format == '.csv':
                download = '[class="text-white-hover bg-brand-hover rounded cursor-pointer full hover-parent hover--inherit sc-bwzfXH iTgcwE"]' 
            else:
                download = '[class="Icon Icon-xlsx Icon__StyledIcon-oj89wd-1 eZysOH"]' 
            with self.page.expect_download(timeout=(self.time*1000)) as download_info:
                self.page.wait_for_selector(download) 
                self.page.click(download,timeout=(self.time*1000))
            download = download_info.value
            for each in self.path:
                download.save_as(each)
            self.close_browser()