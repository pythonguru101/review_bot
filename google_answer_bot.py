import time
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Firefox(proxy='163.172.89.109:1370')
driver.get("https://accounts.google.com/signin")

driver.implicitly_wait(3)

driver.find_element_by_id("identifierId").send_keys("----------------")
driver.find_element_by_id("identifierNext").click()

driver.implicitly_wait(10)
password = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
password.send_keys("----------------")

next_btn = driver.find_element_by_id('passwordNext')
driver.execute_script("arguments[0].click();", next_btn)

time.sleep(80)

driver.get(
    "https://www.google.com/search?authuser=3&q=Tiptop+Restoration+Thousand+Oaks&ludocid=4072880130693755538&lsig=AB86z5XJ6HeUVyZtR9B62-H4vZpH#lpqa=d,2")

SCROLL_PAUSE_TIME = 4


while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height
            continue
