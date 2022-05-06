from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def open_browser(url):
    driver = webdriver.Chrome(ChromeDriverManager().install()) 
    driver.get(url)