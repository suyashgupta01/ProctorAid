from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options

def open_browser(url):
    driver = webdriver.Chrome(ChromeDriverManager().install()) 
    # chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True) # to keep window open :)
    try:
        driver.get(url)
    except:
        driver.get(url) # just reload if ek bar me load na ho
    time.sleep(5) # wait for browser to load :)
    while(True): # to keep the browser window open, else it'll get garbage collected as it's not reference anywhere else in main.py | https://stackoverflow.com/a/47509389/11684146
       pass