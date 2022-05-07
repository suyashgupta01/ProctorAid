from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def open_browser(url):
    my_options = Options()
    # x & y -> to not show "Chrome is being controlled by automated testing software" | https://stackoverflow.com/a/65240100/11684146
    my_options.add_experimental_option("useAutomationExtension", False) # x
    my_options.add_experimental_option("excludeSwitches",["enable-automation"]) # y
    my_options.add_argument('start-maximized')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=my_options) 
    try:
        driver.get(url)
    except:
        driver.get(url) # just reload if ek bar me load na ho
    driver.fullscreen_window()
    time.sleep(5) # wait for browser to load :)
    while(True): # to keep the browser window open, else it'll get garbage collected as it's not reference anywhere else in main.py | https://stackoverflow.com/a/47509389/11684146
       pass

open_browser("https://www.hackerrank.com/test/sample")