import time
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen

data = pd.read_csv('./csv/list.csv')

for d in data.values:
    print("------------", d)
    driver = webdriver.Firefox(proxy='163.172.89.109:1368')
    time.sleep(5)
    driver.get("https://accounts.google.com/signin")
    driver.implicitly_wait(5)

    time.sleep(5)
    try:
        another_account_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), 'Use another account')]")))
        driver.execute_script("arguments[0].click();", another_account_btn)
    except TimeoutException:
        print("No element found")

    time.sleep(5)
    driver.find_element_by_id("identifierId").send_keys(d[0])
    driver.find_element_by_id("identifierNext").click()

    driver.implicitly_wait(5)
    password = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    password.send_keys(d[1])

    next_btn = driver.find_element_by_id('passwordNext')
    driver.execute_script("arguments[0].click();", next_btn)

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
        recover_email_entry.send_keys(d[6])
        next_btn2 = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'Next')]")))
        driver.execute_script("arguments[0].click();", next_btn2)
    except TimeoutException:
        print("No recovery email entry found")

    time.sleep(5)
    try:
        get_verification_code_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@value='Get code']")))
        if get_verification_code_btn:
            driver.quit()
            continue
    except TimeoutException:
        print("No verification code")

    # input GMB
    time.sleep(5)
    driver.get(d[2])

    # fake location
    fake_lat = str(d[4])
    fake_long = str(d[5])

    # Requesting to draw a new map with desired coordinates, and puting the marker
    driver.execute_script("window.navigator.geolocation.getCurrentPosition=function(success){" +
                            "var position = {\"coords\" : {\"latitude\": \""+fake_lat+"\",\"longitude\": \""+fake_long+"\"}};" +
                            "success(position);}")

    time.sleep(10)
    try:
        detail_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                        (By.XPATH, "//a[@id='wrl']")))
        driver.execute_script("arguments[0].click();", detail_btn)
    except TimeoutException:
        print("No add/edit review button found")

    time.sleep(5)
    driver.refresh()

    time.sleep(5)
    try:
        driver.switch_to.frame("goog-reviews-write-widget")
    except NoSuchElementException:
        print("No review write widget found")

    time.sleep(5)
    try:
        five_star_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                         (By.XPATH, "//span[@class='rating']/span[5]")))
        driver.execute_script("arguments[0].click();", five_star_btn)
    except TimeoutException:
        print("No star button found")

    time.sleep(5)
    try:
        text_area = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                         (By.XPATH, "//div[@class='review-text-indent']/textarea")))
        test_review = d[3]
        text_area.send_keys(test_review)
    except TimeoutException:
        print("No textarea found")

    time.sleep(5)
    try:
        driver.find_element_by_xpath("//div[@class='action-publish']").click()
    except NoSuchElementException:
        print("No publish button found")

    # post_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
    #     (By.XPATH, "//div[contains(text(), 'Post')]")))
    # driver.execute_script("arguments[0].click();", post_btn)

    # time.sleep(5)
    # driver.get("https://accounts.google.com/signin")
    #
    # time.sleep(5)
    # driver.find_element_by_xpath("//header[@id='gb']/div[2]/div[3]/div/div[2]").click()
    #
    # time.sleep(5)
    # sign_out_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
    #     (By.XPATH, "//a[contains(text(), 'Sign out')]")))
    # driver.execute_script("arguments[0].click();", sign_out_btn)
    #
    # time.sleep(5)
    # driver.get("https://accounts.google.com/")

    time.sleep(5)
    driver.quit()

