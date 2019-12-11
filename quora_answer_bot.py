import time
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

options = webdriver.FirefoxOptions()
options.add_argument("--kiosk")

profile = webdriver.FirefoxProfile()
profile.set_preference('intl.accept_languages', 'en-US, en, ja')
profile.update_preferences()

proxy_use = '163.172.89.109:1463'
desired_capability = webdriver.DesiredCapabilities.FIREFOX
desired_capability['proxy'] = {
    'proxyType': "manual",
    'httpProxy': proxy_use,
    'ftpProxy': proxy_use,
    'sslProxy': proxy_use,
}

driver = webdriver.Firefox(executable_path='C:\BOT\geckodriver.exe', firefox_options=options, firefox_profile=profile,
                           capabilities=desired_capability)


class AnswerBot(object):
    def __init__(self):
        self.post_qandas()

    def post_qandas(self):
        url = 'https://www.quora.com/'
        driver.get(url)

        qa_response = requests.get('https://beta.matrixcore.io/api/panel/seo/qandas/?is_active=1',
                                headers={'accept': 'application/json',
                                         'Authorization': 'Token 4d69c9b7046b12ea7848b8c47be7df4fc2914a30'})
        qa_data = qa_response.json()
        qa_results = qa_data['results']

        user_response = requests.get('https://beta.matrixcore.io/api/panel/seo/accounts/?is_active=1&provider=quora',
                                headers={'accept': 'application/json',
                                         'Authorization': 'Token 4d69c9b7046b12ea7848b8c47be7df4fc2914a30'})
        user_data = user_response.json()
        user_results = user_data['results']

        email_entry = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='form_inputs']/div[@class='form_column'][1]/input")))
        email_entry.send_keys("************")

        password_entry = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='form_inputs']/div[@class='form_column'][2]/input")))
        password_entry.send_keys("************")

        login_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='form_inputs']/div[@class='form_column'][3]/input[@value='Login']")))
        driver.execute_script("arguments[0].click();", login_btn)

        f = open("answer.txt", 'r')
        answer_list = f.readlines()
        f.close()

        for i in range(len(answer_list)):
            item = answer_list[i]
            item_url = str(item).split('&', -1)[0]
            item_answer = str(item).split('&', -1)[1]
            # print("url, answer", url, answer)
            time.sleep(10)
            driver.get(item_url)

            time.sleep(10)
            start_answer_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='More options']")))
            driver.execute_script("arguments[0].click();", start_answer_btn)

            time.sleep(10)
            click_answer_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Answer Anonymously')]")))
            driver.execute_script("arguments[0].click();", click_answer_btn)

            time.sleep(5)
            answer_entry = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='doc empty']")))
            answer_entry.send_keys(item_answer)

            time.sleep(3)
            submit_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//a[@class='submit_button']")))
            driver.execute_script("arguments[0].click();", submit_btn)

            time.sleep(3)
            done_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(text(), 'Done')]")))
            driver.execute_script("arguments[0].click();", done_btn)

            time.sleep(3)

    @staticmethod
    def make_request(url):
        headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36.'
        }
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            return r


if __name__ == "__main__":
    AnswerBot()
