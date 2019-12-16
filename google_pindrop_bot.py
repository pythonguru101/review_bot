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
from selenium.common.exceptions import NoSuchElementException

data = pd.read_csv('pindrop.csv')

for d in data.values:
    print("********", d)

    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', 'en-US, en, ja')
    profile.update_preferences()

    # proxy_use = '163.172.89.109:1468'
    # desired_capability = webdriver.DesiredCapabilities.FIREFOX
    # desired_capability['proxy'] = {
    #     'proxyType': "manual",
    #     'httpProxy': proxy_use,
    #     'ftpProxy': proxy_use,
    #     'sslProxy': proxy_use,
    # }

    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get("https://accounts.google.com/signin")

    driver.implicitly_wait(3)
    driver.find_element_by_id("identifierId").send_keys(d[0])
    driver.find_element_by_id("identifierNext").click()

    driver.implicitly_wait(5)
    password = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    password.send_keys(d[1])

    driver.implicitly_wait(5)
    next_btn = driver.find_element_by_id('passwordNext')
    driver.execute_script("arguments[0].click();", next_btn)

    # Google captcha
    time.sleep(5)
    image = driver.find_element_by_id('captchaimg').get_attribute("src")
    print("Image url: ", image)

    # get the image source
    time.sleep(5)
    f = open("./img/captcha.jpeg", 'wb')
    f.write(urlopen(image).read())
    f.close()

    # scrape captcha string
    from python_anticaptcha import AnticaptchaClient, ImageToTextTask
    api_key = 'f12634370974461a767a103936917e6c'
    captcha_fp = open("./img/captcha.jpeg", 'rb')
    client = AnticaptchaClient(api_key)
    task = ImageToTextTask(captcha_fp)
    job = client.createTask(task)
    job.join()
    print("Captchar string: ", job.get_captcha_text())

    # input security password and captcha
    time.sleep(5)
    password_entry = driver.find_element_by_name("password").send_keys(d[1])
    captchar_entry = driver.find_element_by_id("ca").send_keys(job.get_captcha_text())
    print("=========password, captchar==========", d[1], job.get_captcha_text())
    next_btn = driver.find_element_by_id('passwordNext')
    driver.execute_script("arguments[0].click();", next_btn)
    # -----------------------------

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
    driver.get("https://www.google.com/maps/place/")

    time.sleep(5)
    location_search_entry = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='searchboxinput']")))
    location_search_entry.send_keys(d[3], Keys.ENTER)

    time.sleep(10)
    add_place_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Add a missing place')]")))
    driver.execute_script("arguments[0].click();", add_place_btn)

    time.sleep(5)
    driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[-1])

    time.sleep(5)
    add_name_entry = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(), 'Add name')]/ancestor::div/input")))
    add_name_entry.send_keys(d[4])

    time.sleep(5)
    add_category_entry = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(), 'Add category')]/ancestor::div/input")))
    add_category_entry.send_keys(d[5], Keys.ARROW_DOWN, Keys.ENTER)

    time.sleep(5)
    xpath_str = "//div[@data-display-value='" + d[5] + "']"
    data_display_item = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, xpath_str)))
    driver.execute_script("arguments[0].click();", data_display_item)

    time.sleep(5)
    add_infos = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(), 'Add phone, hours, website, opening date and photos')]")))
    driver.execute_script("arguments[0].click();", add_infos)

    time.sleep(5)
    add_open_date = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(), 'Add opening date')]")))
    driver.execute_script("arguments[0].click();", add_open_date)

    # month #
    time.sleep(5)
    month_select = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@data-tooltip='Month']/div[1]")))
    driver.execute_script("arguments[0].click();", month_select)

    time.sleep(5)
    month_xpath = "//span[contains(text(), '" + str(d[6]).split(" ")[0] + "')]"
    month_item_select = driver.find_elements_by_xpath(month_xpath)
    driver.execute_script("arguments[0].click();", month_item_select[1])

    time.sleep(5)
    specific_day = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, "//label[contains(text(), 'Add the specific day')]")))
    driver.execute_script("arguments[0].click();", specific_day)

    # day #
    time.sleep(5)
    day_select = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@data-tooltip='Day']/div[1]")))
    driver.execute_script("arguments[0].click();", day_select)

    time.sleep(5)
    day_xpath = "//span[contains(text(), '" + str(d[6]).split(" ", -1)[1] + "')]"
    day_item_select = driver.find_elements_by_xpath(day_xpath)
    driver.execute_script("arguments[0].click();", day_item_select[1])

    # year #
    time.sleep(5)
    year_select = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@data-tooltip='Year']/div[1]")))
    driver.execute_script("arguments[0].click();", year_select)

    time.sleep(5)
    year_xpath = "//span[contains(text(), '" + str(d[6]).split(" ", -1)[2] + "')]"
    year_item_select = driver.find_elements_by_xpath(year_xpath)
    driver.execute_script("arguments[0].click();", year_item_select[1])

    time.sleep(5)
    done_btn = driver.find_element_by_xpath("//span[contains(text(), 'Done')]")
    driver.execute_script("arguments[0].click();", done_btn)

    # add phone number #
    time.sleep(5)
    tel_entry = driver.find_element_by_xpath("//input[@type='tel']")
    tel_entry.send_keys(d[7])

    # add hours of service #
    time.sleep(5)
    add_hours_btn = driver.find_element_by_xpath("//div[contains(text(), 'Add hours')]")
    driver.execute_script("arguments[0].click();", add_hours_btn)

    # Sunday
    time.sleep(5)
    sunday_btn = driver.find_element_by_xpath("//div[contains(text(), 'Sunday')]")
    driver.execute_script("arguments[0].click();", sunday_btn)

    time.sleep(5)
    sunday_entry_from = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Opening time on Sunday']")))
    sunday_entry_from.clear()
    sunday_line = str(d[8]).split("\n")[0]
    sunday_entry_from.send_keys(str(sunday_line).split(',')[1], Keys.ENTER)

    time.sleep(5)
    sunday_entry_to = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Closing time on Sunday']")))
    sunday_entry_to.clear()
    sunday_entry_to.send_keys(str(sunday_line).split(',')[2], Keys.ENTER)

    # Monday
    time.sleep(5)
    monday_btn = driver.find_element_by_xpath("//div[contains(text(), 'Monday')]")
    driver.execute_script("arguments[0].click();", monday_btn)

    time.sleep(5)
    monday_entry_from = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Opening time on Monday']")))
    monday_entry_from.clear()
    monday_line = str(d[8]).split("\n")[1]
    monday_entry_from.send_keys(str(monday_line).split(',')[1], Keys.ENTER)

    time.sleep(5)
    monday_entry_to = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Closing time on Monday']")))
    monday_entry_to.clear()
    monday_entry_to.send_keys(str(monday_line).split(',')[2], Keys.ENTER)

    # Tuesday
    time.sleep(5)
    tuesday_btn = driver.find_element_by_xpath("//div[contains(text(), 'Tuesday')]")
    driver.execute_script("arguments[0].click();", tuesday_btn)

    time.sleep(5)
    tuesday_entry_from = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Opening time on Tuesday']")))
    tuesday_entry_from.clear()
    tuesday_line = str(d[8]).split("\n")[2]
    tuesday_entry_from.send_keys(str(tuesday_line).split(',')[1], Keys.ENTER)

    time.sleep(5)
    tuesday_entry_to = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Closing time on Tuesday']")))
    tuesday_entry_to.clear()
    tuesday_entry_to.send_keys(str(tuesday_line).split(',')[2], Keys.ENTER)

    # Wednesday
    time.sleep(5)
    wednesday_btn = driver.find_element_by_xpath("//div[contains(text(), 'Wednesday')]")
    driver.execute_script("arguments[0].click();", wednesday_btn)

    time.sleep(5)
    wednesday_entry_from = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Opening time on Wednesday']")))
    wednesday_entry_from.clear()
    wednesday_line = str(d[8]).split("\n")[3]
    wednesday_entry_from.send_keys(str(wednesday_line).split(',')[1], Keys.ENTER)

    time.sleep(5)
    wednesday_entry_to = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Closing time on Wednesday']")))
    wednesday_entry_to.clear()
    wednesday_entry_to.send_keys(str(wednesday_line).split(',')[2], Keys.ENTER)

    # Thursday
    time.sleep(5)
    thursday_btn = driver.find_element_by_xpath("//div[contains(text(), 'Thursday')]")
    driver.execute_script("arguments[0].click();", thursday_btn)

    time.sleep(5)
    thursday_entry_from = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Opening time on Thursday']")))
    thursday_entry_from.clear()
    thursday_line = str(d[8]).split("\n")[4]
    thursday_entry_from.send_keys(str(thursday_line).split(',')[1], Keys.ENTER)

    time.sleep(5)
    thursday_entry_to = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Closing time on Thursday']")))
    thursday_entry_to.clear()
    thursday_entry_to.send_keys(str(thursday_line).split(',')[2], Keys.ENTER)

    # Friday
    time.sleep(5)
    friday_btn = driver.find_element_by_xpath("//div[contains(text(), 'Friday')]")
    driver.execute_script("arguments[0].click();", friday_btn)

    time.sleep(5)
    friday_entry_from = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Opening time on Friday']")))
    friday_entry_from.clear()
    friday_line = str(d[8]).split("\n")[5]
    friday_entry_from.send_keys(str(friday_line).split(',')[1], Keys.ENTER)

    time.sleep(5)
    friday_entry_to = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Closing time on Friday']")))
    friday_entry_to.clear()
    friday_entry_to.send_keys(str(friday_line).split(',')[2], Keys.ENTER)

    # Saturday
    time.sleep(5)
    saturday_btn = driver.find_element_by_xpath("//div[contains(text(), 'Saturday')]")
    driver.execute_script("arguments[0].click();", saturday_btn)

    time.sleep(5)
    saturday_entry_from = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Opening time on Saturday']")))
    saturday_entry_from.clear()
    saturday_line = str(d[8]).split("\n")[6]
    saturday_entry_from.send_keys(str(saturday_line).split(',')[1], Keys.ENTER)

    time.sleep(5)
    saturday_entry_to = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//input[@aria-label='Closing time on Saturday']")))
    saturday_entry_to.clear()
    saturday_entry_to.send_keys(str(saturday_line).split(',')[2], Keys.ENTER)

    # Done button
    time.sleep(5)
    done2_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        "//span[contains(text(), 'Done')]")))
    driver.execute_script("arguments[0].click();", done2_btn)

    time.sleep(5)
    send_btn = driver.find_element_by_xpath("//span[contains(text(), 'Send')]")
    driver.execute_script("arguments[0].click();", send_btn)

    time.sleep(5)
    driver.switch_to.default_content()

    time.sleep(5)
    contribute_btn = driver.find_element_by_xpath("//button[contains(text(), 'Contribute more')]")
    driver.execute_script("arguments[0].click();", contribute_btn)

    time.sleep(5)
    edits_btn = driver.find_element_by_xpath("//button[@data-tooltip='Edits']")
    driver.execute_script("arguments[0].click();", edits_btn)

    time.sleep(5)
    driver.quit()
