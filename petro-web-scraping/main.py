import utils
import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(executable_path="petro-web-scraping\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.mymesra.com.my/petrol-station-finder")

list_of_outlets_uncleaned = []
WebDriverWait(driver, 8).until(
    EC.presence_of_element_located((By.CLASS_NAME, "onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon"))
)
cancel_button = driver.find_element(By.CLASS_NAME, "onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon")
cancel_button.click()

WebDriverWait(driver, 8).until(
    EC.presence_of_element_located((By.CLASS_NAME, "aps-0030-so-wrapper.hvr-normal.font-822FA4B9-B520-451A-81C4-72392A0A53E2.btn-padding-custom.font-icon-textless.aps-0030-so-wrapper-3feda368-3628-45a9-be67-862a3dd828a4"))
)
filter_button = driver.find_element(By.CLASS_NAME, "aps-0030-so-wrapper.hvr-normal.font-822FA4B9-B520-451A-81C4-72392A0A53E2.btn-padding-custom.font-icon-textless.aps-0030-so-wrapper-3feda368-3628-45a9-be67-862a3dd828a4")
filter_button.click()

WebDriverWait(driver, 8).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='pnl-filter']/div/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div/div/div[1]/ul/li[3]/label/span[1]/img"))
)
option_1 = driver.find_element(By.XPATH, "//*[@id='pnl-filter']/div/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div/div/div[1]/ul/li[3]/label/span[1]/img")
option_1.click()

WebDriverWait(driver, 8).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='btn-apply-filter']/a"))
)
apply_button = driver.find_element(By.XPATH, "//*[@id='btn-apply-filter']/a")
apply_button.click()

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='x-autocp']/div/div[1]/input"))
)

input_element = driver.find_element(By.XPATH, "//*[@id='x-autocp']/div/div[1]/input")
input_element.click()
input_element.clear()
input_element.send_keys(utils.states[0])

# This clicks the first option in the google auto-complete dropdown
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='htmltag']/body/div[14]/div[1]"))
)
auto_complete = driver.find_element(By.XPATH, "//*[@id='htmltag']/body/div[14]/div[1]")
auto_complete.click()

#//*[@id="lst-assets"]/div/div[1]/div[1]/div/div/div/div[1]/div/div[2]/div/div[1]/div (item 1)
#//*[@id="lst-assets"]/div/div[1]/div[2]/div/div/div/div[1]/div/div[2]/div/div[1]/div (item 2)
#//*[@id="lst-assets"]/div/div[1]/div[3]/div/div/div/div[1]/div/div[2]/div/div[1]/div (item 3)

# Looper = True
# while Looper:
#     try:
#         WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located((By.XPATH, "//*[@id='lst-assets']/div/div[2]/a[4]"))
#     )
#         next_button = driver.find_element(By.XPATH, "//*[@id='lst-assets']/div/div[2]/a[4]")
#         print("Next button found")
#         time.sleep(5)
#         for i in range(9):
#             nama_taman = driver.find_element(By.XPATH, f"//*[@id='lst-assets']/div/div[1]/div[{i+1}]/div/div/div/div[1]/div/div[2]/div/div[1]/div").text
#             list_of_outlets_uncleaned.append(nama_taman)
#         next_button.click()
#         Looper = True
#     except: 
#         print("No next button found")
#         looper = False
#         break
time.sleep(3)
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='lst-assets']/div/div[2]/a[4]"))
)
j = 0
while driver.find_elements(By.XPATH, "//*[@id='lst-assets']/div/div[2]/a[4]") and j < 5:
    time.sleep(3)
    for i in range(9):
        nama_taman = driver.find_element(By.XPATH, f"//*[@id='lst-assets']/div/div[1]/div[{i+1}]/div/div/div/div[1]/div/div[2]/div/div[1]/div").text
        list_of_outlets_uncleaned.append(nama_taman)
    next_button = driver.find_element(By.XPATH, "//*[@id='lst-assets']/div/div[2]/a[4]")
    try:
        next_button.click()
    except:
        break
    j += 1

print(list_of_outlets_uncleaned)
time.sleep(10)
driver.quit()