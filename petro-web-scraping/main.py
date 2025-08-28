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
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.mymesra.com.my/petrol-station-finder")

list_of_outlets_uncleaned = []
WebDriverWait(driver, 8).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon"))
)
cancel_button = driver.find_element(By.CLASS_NAME, "onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon")
cancel_button.click()

def filter_press():
    WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.CLASS_NAME, "aps-0030-so-wrapper.hvr-normal.font-822FA4B9-B520-451A-81C4-72392A0A53E2.btn-padding-custom.font-icon-textless.aps-0030-so-wrapper-3feda368-3628-45a9-be67-862a3dd828a4"))
    )
    filter_button = driver.find_element(By.CLASS_NAME, "aps-0030-so-wrapper.hvr-normal.font-822FA4B9-B520-451A-81C4-72392A0A53E2.btn-padding-custom.font-icon-textless.aps-0030-so-wrapper-3feda368-3628-45a9-be67-862a3dd828a4")
    filter_button.click()

def option_press(xpath):
    WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    option_1 = driver.find_element(By.XPATH, xpath)
    option_1.click()

def apply_press():
    WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='btn-apply-filter']/a"))
    )
    apply_button = driver.find_element(By.XPATH, "//*[@id='btn-apply-filter']/a")
    apply_button.click()

def searchbar(i):
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='x-autocp']/div/div[1]/input"))
    )
    input_element = driver.find_element(By.XPATH, "//*[@id='x-autocp']/div/div[1]/input")
    input_element.click() # click on search bar
    input_element.clear() # clear it
    input_element.send_keys(utils.states[i]) #select thing to type
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='htmltag']/body/div[13]/div[1]/span[2]"))
    )
    auto_complete = driver.find_element(By.XPATH, "//*[@id='htmltag']/body/div[13]/div[1]/span[2]")
    auto_complete.click()

#//*[@id="lst-assets"]/div/div[1]/div[1]/div/div/div/div[1]/div/div[2]/div/div[1]/div (outlet name 1)
#//*[@id="lst-assets"]/div/div[1]/div[2]/div/div/div/div[1]/div/div[2]/div/div[1]/div (outlet name 2)
#//*[@id="lst-assets"]/div/div[1]/div[3]/div/div/div/div[1]/div/div[2]/div/div[1]/div (outlet name 3)
#//*[@id="lst-assets"]/div/div[1]/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div (outlet address 1)
#//*[@id="lst-assets"]/div/div[1]/div[2]/div/div/div/div[1]/div/div[2]/div/div[2]/div (outlet address 2)
#//*[@id="lst-assets"]/div/div[1]/div[3]/div/div/div/div[1]/div/div[2]/div/div[2]/div (outlet address 3)

def exhaust_pages():
    time.sleep(2)
    driver.find_element(By.XPATH, '//body').send_keys(Keys.CONTROL + Keys.END)
    try:
        WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='lst-assets']/div/div[2]/a[4]"))
        )
    except:
        pass
    j = 0
    while (driver.find_elements(By.XPATH, "//*[@id='lst-assets']/div/div[2]/a[4]") and j < 5) or j == 0:
        time.sleep(2)
        for i in range(9):
            try:
                nama_taman = driver.find_element(By.XPATH, f"//*[@id='lst-assets']/div/div[1]/div[{i+1}]/div/div/div/div[1]/div/div[2]/div/div[1]/div").text
                address_taman = driver.find_element(By.XPATH, f"//*[@id='lst-assets']/div/div[1]/div[{i+1}]/div/div/div/div[1]/div/div[2]/div/div[2]/div").text
            except:
                pass
            try:
                list_of_outlets_uncleaned.append([nama_taman, address_taman])
            except:
                pass
        try:
            next_button = driver.find_element(By.XPATH, "//*[@id='lst-assets']/div/div[2]/a[4]")
        except:
            pass
        try:
            next_button.click()
        except:
            break
        j += 1

time.sleep(7)
print("Number of States: ", len(utils.states))
for key in utils.categories:
    driver.refresh()
    print(f"Category: {key}\n","="*40)
    time.sleep(5)
    filter_press()
    option_press(utils.categories[key])
    apply_press()
    for p in range(len(utils.states)):
        print("State: ", utils.states[p])
        searchbar(p)
        exhaust_pages()
        time.sleep(1)
        driver.find_element(By.XPATH, '//body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(1)

n=1
full_list = pd.DataFrame(list_of_outlets_uncleaned).drop_duplicates().reset_index(drop=True)
full_list.to_excel("petro-web-scraping\mesraoutletsperwebsite.xlsx")
print(full_list)
time.sleep(10)
driver.quit()