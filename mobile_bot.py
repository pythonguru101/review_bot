import mobile_agent

import time
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", mobile_agent.get_random_agent())

driver = webdriver.Firefox(profile, proxy='163.172.89.109:1368')
driver.get("https://accounts.google.com/signin")

driver.implicitly_wait(3)

driver.find_element_by_id("identifierId").send_keys("-----------------")
driver.find_element_by_id("identifierNext").click()

driver.implicitly_wait(10)
password = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
password.send_keys("-------------")

next_btn = driver.find_element_by_id('passwordNext')
driver.execute_script("arguments[0].click();", next_btn)

time.sleep(80)

driver.get("https://www.google.com/maps/reviews/@34.1794909,-118.8748677,17z/data=!3m1!4b1!4m5!14m4!1m3!1m2!1s111078506884794246891!2s0x80c297fef4443435:0x3885c6e65abf7292?hl=en-US")

time.sleep(5)
continue_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Accept & continue')]")))
driver.execute_script("arguments[0].click();", continue_btn)

time.sleep(5)
detail_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Place details')]")))
driver.execute_script("arguments[0].click();", detail_btn)

time.sleep(5)
driver.refresh()

time.sleep(5)
write_review_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@data-value='Write a review']")))
driver.execute_script("arguments[0].click();", write_review_btn)

time.sleep(5)
five_star_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                 (By.XPATH, "//span[@class='rating']/span[5]")))
driver.execute_script("arguments[0].click();", five_star_btn)

time.sleep(5)
text_area = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                 (By.XPATH, "//div[@class='review-text-indent']")))
text_area.send_keys("This is the sample review")
time.sleep(5)