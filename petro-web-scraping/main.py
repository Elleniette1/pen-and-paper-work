import utils
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service(executable_path="petro-web-scraping\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.mymesra.com.my/petrol-station-finder")

time.sleep(5)

driver.quit()