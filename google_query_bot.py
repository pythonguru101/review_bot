import time
import requests
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from urllib.request import urlopen

data = pd.read_csv('query.csv')

for d in data.values:
    print("********", d)

    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', 'en-US, en, ja')
    profile.update_preferences()

    proxy_use = d[8]
    desired_capability = webdriver.DesiredCapabilities.FIREFOX
    desired_capability['proxy'] = {
        'proxyType': "manual",
        'httpProxy': proxy_use,
        'ftpProxy': proxy_use,
        'sslProxy': proxy_use,
    }

    driver = webdriver.Firefox(executable_path="C:\BOT\geckodriver.exe", firefox_profile=profile,
                               capabilities=desired_capability)
    driver.get("https://accounts.google.com/signin")

    driver.implicitly_wait(3)
    driver.find_element_by_id("identifierId").send_keys(d[0])
    driver.find_element_by_id("identifierNext").click()

    driver.implicitly_wait(10)
    password = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    password.send_keys(d[1])

    next_btn = driver.find_element_by_id('passwordNext')
    driver.execute_script("arguments[0].click();", next_btn)

    # Google captcha
    # time.sleep(5)
    # image = driver.find_element_by_id('captchaimg').get_attribute("src")
    # print("Image url: ", image)
    #
    # # get the image source
    # time.sleep(5)
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
    # time.sleep(5)
    # password_entry = driver.find_element_by_name("password").send_keys(d[1])
    # captchar_entry = driver.find_element_by_id("ca").send_keys(job.get_captcha_text())
    # print("=========password, captchar==========", d[1], job.get_captcha_text())
    # next_btn = driver.find_element_by_id('passwordNext')
    # driver.execute_script("arguments[0].click();", next_btn)
    # ---------------

    time.sleep(5)
    try:
        confirm_recover_email_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), 'Confirm your recovery email')]")))
        driver.execute_script("arguments[0].click();", confirm_recover_email_btn)
    except TimeoutException:
        print("No confirm recovery email button found")

    time.sleep(5)
    try:
        recover_email_entry = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@id='knowledge-preregistered-email-response']")))
        recover_email_entry.send_keys(d[2])
        next_btn2 = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'Next')]")))
        driver.execute_script("arguments[0].click();", next_btn2)
    except TimeoutException:
        print("No recovery email entry found")

    time.sleep(5)
    driver.get("https://www.google.com/webhp")

    time.sleep(5)
    # fake location
    fake_lat = str(d[6])
    fake_long = str(d[7])

    # Requesting to draw a new map with desired coordinates, and puting the marker
    driver.execute_script("window.navigator.geolocation.getCurrentPosition=function(success){" +
                          "var position = {\"coords\" : {\"latitude\": \"" + fake_lat + "\",\"longitude\": \"" + fake_long + "\"}};" +
                          "success(position);}")

    time.sleep(5)
    google_search_entry = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@title='Search']")))
    google_search_entry.send_keys(d[3], Keys.ENTER)

    SCROLL_PAUSE_TIME = 4
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight/4")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight/4")
        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight/4")
            if new_height == last_height:
                break
            else:
                last_height = new_height
                continue

    try:
        time.sleep(5)
        more_about_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(), 'More about')]")))
        driver.execute_script("arguments[0].click();", more_about_btn)
    except TimeoutException:
        print("No more about button found")

    try:
        time.sleep(5)
        ask_question_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'Ask a question')]")))
        driver.execute_script("arguments[0].click();", ask_question_btn)
    except TimeoutException:
        print("No ask question button found")

    try:
        time.sleep(5)
        text_area = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                (By.XPATH, "//textarea[@placeholder='Ask a question or get advice from the owner and broader community.']")))
        text_area.send_keys(d[4])
    except TimeoutException:
        print("No textarea found")

    try:
        time.sleep(5)
        post_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'POST')]")))
        driver.execute_script("arguments[0].click();", post_btn)
    except TimeoutException:
        print("No post button found")

    time.sleep(5)
    driver.quit()
