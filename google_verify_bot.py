import time
import requests
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.request import urlopen

data = pd.read_csv('postcards.csv')

for d in data.values:
    print("********", d)

    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', 'en-US, en, ja')
    profile.update_preferences()

    driver = webdriver.Firefox(executable_path="C:\BOT\geckodriver.exe", firefox_profile=profile)
    driver.get("https://business.google.com/locations?hl=en")

    time.sleep(3)
    try:
        another_account_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), 'Use another account')]")))
        driver.execute_script("arguments[0].click();", another_account_btn)
    except TimeoutException:
        print("No element found")

    time.sleep(3)
    driver.find_element_by_id("identifierId").send_keys(d[0])
    driver.find_element_by_id("identifierNext").click()

    driver.implicitly_wait(3)
    password = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    password.send_keys(d[1])

    next_btn = driver.find_element_by_id('passwordNext')
    driver.execute_script("arguments[0].click();", next_btn)

    # time.sleep(3)
    # image = driver.find_element_by_id('captchaimg').get_attribute("src")
    # print("Image url: ", image)
    #
    # # get the image source
    # time.sleep(3)
    # f = open("./img/captcha.jpeg", 'wb')
    # f.write(urlopen(image).read())
    # f.close()
    #
    # # scrape captcha string
    # from python_anticaptcha import AnticaptchaClient, ImageToTextTask
    # api_key = 'f12634370974461a767a103936917e6c'
    # captcha_fp = open("./img/captcha.jpeg", 'rb')
    # client = AnticaptchaClient(api_key)
    # task = ImageToTextTask(captcha_fp)
    # job = client.createTask(task)
    # job.join()
    # print("Captchar string: ", job.get_captcha_text())
    #
    # # input security password and captcha
    # time.sleep(3)
    # password_entry = driver.find_element_by_name("password").send_keys(d[1])
    # captchar_entry = driver.find_element_by_id("ca").send_keys(job.get_captcha_text())
    # print("=========password, captchar==========", d[1], job.get_captcha_text())
    # next_btn = driver.find_element_by_id('passwordNext')
    # driver.execute_script("arguments[0].click();", next_btn)

    time.sleep(3)
    try:
        confirm_recover_email_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), 'Confirm your recovery email')]")))
        driver.execute_script("arguments[0].click();", confirm_recover_email_btn)
    except TimeoutException:
        print("No confirm recovery email button found")

    time.sleep(3)
    try:
        recover_email_entry = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@id='knowledge-preregistered-email-response']")))
        recover_email_entry.send_keys(d[2])
        next_btn2 = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'Next')]")))
        driver.execute_script("arguments[0].click();", next_btn2)
    except TimeoutException:
        print("No recovery email entry found")

    # time.sleep(5)
    # try:
    #     get_verification_code_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
    #         (By.XPATH, "//input[@value='Get code']")))
    #     if get_verification_code_btn:
    #         driver.quit()
    #         continue
    # except TimeoutException:
    #     print("No verification code")

    # fake location
    fake_lat = str(d[3])
    fake_long = str(d[4])

    # Requesting to draw a new map with desired coordinates, and puting the marker
    driver.execute_script("window.navigator.geolocation.getCurrentPosition=function(success){" +
                            "var position = {\"coords\" : {\"latitude\": \""+fake_lat+"\",\"longitude\": \""+fake_long+"\"}};" +
                            "success(position);}")

    time.sleep(3)
    try:
        location_item = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                        (By.XPATH, "//span[@class='hwl8wd']")))
        driver.execute_script("arguments[0].click();", location_item)
    except TimeoutException:
        print("No location item found")

    time.sleep(3)
    try:
        info_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                         (By.XPATH, "//span[contains(text(), 'Info')]")))
        driver.execute_script("arguments[0].click();", info_btn)
    except TimeoutException:
        print("No Info button found")

    time.sleep(3)
    try:
        phone_entry = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                         (By.XPATH, "//div[@jsname='qF9wee']")))
        driver.execute_script("arguments[0].click();", phone_entry)
    except TimeoutException:
        print("No phone entry found")

    time.sleep(3)
    try:
        phone_entry2 = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                         (By.XPATH, "//input[@type='tel']")))
        phone_entry2.send_keys(d[5])
    except NoSuchElementException:
        print("No phone2 entry found")

    time.sleep(3)
    try:
        apply_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@data-id='EBS5u']")))
        driver.execute_script("arguments[0].click();", apply_btn)
    except TimeoutException:
        print("No apply button found")

    time.sleep(3)
    driver.quit()
