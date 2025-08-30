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
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton

# ======================================IMPORTANT XPATH STRUCTURES======================================
#//*[@id="lst-assets"]/div/div[1]/div[1]/div/div/div/div[1]/div/div[2]/div/div[1]/div (outlet name 1)
#//*[@id="lst-assets"]/div/div[1]/div[2]/div/div/div/div[1]/div/div[2]/div/div[1]/div (outlet name 2)
#//*[@id="lst-assets"]/div/div[1]/div[3]/div/div/div/div[1]/div/div[2]/div/div[1]/div (outlet name 3)
#//*[@id="lst-assets"]/div/div[1]/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div (outlet address 1)
#//*[@id="lst-assets"]/div/div[1]/div[2]/div/div/div/div[1]/div/div[2]/div/div[2]/div (outlet address 2)
#//*[@id="lst-assets"]/div/div[1]/div[3]/div/div/div/div[1]/div/div[2]/div/div[2]/div (outlet address 3)
# ======================================================================================================

# ============================== Basic Setup + Reading any Prior Files =================================
service = Service(executable_path="petro-web-scraping\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(service=service, options=options)
action = ActionBuilder(driver)
driver.get("https://www.mymesra.com.my/petrol-station-finder")

# Closing Cookies Popup
WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon"))
)
cancel_button = driver.find_element(By.CLASS_NAME, "onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon")
cancel_button.click()

# Functions
def option_press(xpath):
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "aps-0030-so-wrapper.hvr-normal.font-822FA4B9-B520-451A-81C4-72392A0A53E2.btn-padding-custom.font-icon-textless.aps-0030-so-wrapper-3feda368-3628-45a9-be67-862a3dd828a4"))
    )
    filter_button = driver.find_element(By.CLASS_NAME, "aps-0030-so-wrapper.hvr-normal.font-822FA4B9-B520-451A-81C4-72392A0A53E2.btn-padding-custom.font-icon-textless.aps-0030-so-wrapper-3feda368-3628-45a9-be67-862a3dd828a4")
    filter_button.click()
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )
    option = driver.find_element(By.XPATH, xpath)
    option.click()
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='btn-apply-filter']/a"))
    )
    apply_button = driver.find_element(By.XPATH, "//*[@id='btn-apply-filter']/a")
    apply_button.click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "page-transition-cover.preload-cover"))
    )
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "page-transition-cover.preload-cover"))
    )

def searchbar(xtown):
    driver.find_element(By.XPATH, '//body').send_keys(Keys.CONTROL + Keys.HOME)
    action.pointer_action.move_to_location(0, 0)
    action.perform()
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='x-autocp']/div/div[1]/input"))
    )
    input_bar = driver.find_element(By.XPATH, "//*[@id='x-autocp']/div/div[1]/input")
    input_bar.click()
    input_bar.clear()
    input_bar.send_keys(utils.states[xtown])
    while True:
        try:
            driver.find_element(By.XPATH, '//body').send_keys(Keys.CONTROL + Keys.HOME)
            action.pointer_action.move_to_location(0, 0)
            input_bar.click()
            WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='htmltag']/body/div[13]/div[1]/span[2]"))
            )
            auto_complete = driver.find_element(By.XPATH, "//*[@id='htmltag']/body/div[13]/div[1]/span[2]")
            auto_complete.click()
            break
        except:
            driver.find_element(By.XPATH, '//body').send_keys(Keys.CONTROL + Keys.HOME)
            action.pointer_action.move_to_location(0, 0)
            
            try:
                driver.find_element(By.XPATH, '//body').send_keys(Keys.CONTROL + Keys.HOME)
                action.pointer_action.move_to_location(0, 0)
                action.perform()
                input_bar.click()
                WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='htmltag']/body/div[14]/div[1]/span[2]"))
                )
                auto_complete = driver.find_element(By.XPATH, "//*[@id='htmltag']/body/div[14]/div[1]/span[2]")
                auto_complete.click()
            except:
                pass
            pass
        

def exhaust_pages():
    try:
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "page-transition-cover.preload-cover"))
        )
        WebDriverWait(driver, 15).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "page-transition-cover.preload-cover"))
        )
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='lst-assets']/div/div[1]/div[1]/div/div/div/div[1]/div/div[2]/div/div[1]/div"))
        )
        bandar = str(driver.find_element(By.XPATH, "//*[@id='lbl-looking-for']/div/div").text)
        bandar = bandar.split("Your location is ")[1].split(". Here is what you are looking for:")[0]
        while True:
            for i in range(9):
                try:
                    nama_outlet = driver.find_element(By.XPATH, f"//*[@id='lst-assets']/div/div[1]/div[{i+1}]/div/div/div/div[1]/div/div[2]/div/div[1]/div").text
                    address_outlet = driver.find_element(By.XPATH, f"//*[@id='lst-assets']/div/div[1]/div[{i+1}]/div/div/div/div[1]/div/div[2]/div/div[2]/div").text
                    print(nama_outlet, address_outlet)
                    list_of_outlets_uncleaned.append([nama_outlet, address_outlet, bandar])
                except:
                    break
            try:
                WebDriverWait(driver, 0.2).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "next_link"))
                )
                next_button = driver.find_element(By.CLASS_NAME, "next_link")
                next_button.click()
                WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "page-transition-cover.preload-cover"))
                )
                WebDriverWait(driver, 15).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "page-transition-cover.preload-cover"))
                )
            except:
                break
    except:
        return
    pass

# ==================================== MAIN PROGRAM ==============================================
t = 1

#category = "fnb"
for category in utils.categories:
    time.sleep(5)
    list_of_outlets_uncleaned = []
    print("Number of Towns: ", len(utils.states))
    key = utils.categories[category]
    driver.refresh()
    time.sleep(1)
    print(f"Category: {category}\n","="*40)
    option_press(key)

    for town in range(0,len(utils.states),1):
        print(f"{t}. Searching Town: ", utils.states[town])
        searchbar(town)
        exhaust_pages()
        t += 1

    a = pd.DataFrame(list_of_outlets_uncleaned).drop_duplicates(subset=[0,1]).reset_index(drop=True)
    print("Number of Unique Rows: ", a.shape[0])
    b = pd.DataFrame()
    b[category] = a.shape[0]
    a.drop(0, axis=1).to_excel(f"petro-web-scraping\petronasfinalfiles\mesraoutlets-up-to-{category}.xlsx")
# ===============================================================================================

# ==================================== FINAL CLEANUP & EXPORT ===================================
print(b)
driver.quit()
# ===============================================================================================