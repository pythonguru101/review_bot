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

driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver', firefox_options=options, proxy='163.172.89.109:1366')
# driver.maximize_window()


class SeleniumBot(object):

    def __init__(self):
        self.post_qandas()

    def post_qandas(self):
        url = 'https://www.quora.com/'
        # r = self.make_request(url)
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
        for i in range(len(user_results)):
            print("username, password = ", user_data['results'][i]['username'], user_data['results'][i]['password'])

        email_entry = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='form_inputs']/div[@class='form_column'][1]/input")))
        email_entry.send_keys("---------------")

        password_entry = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='form_inputs']/div[@class='form_column'][2]/input")))
        password_entry.send_keys("----------------")

        login_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='form_inputs']/div[@class='form_column'][3]/input[@value='Login']")))
        driver.execute_script("arguments[0].click();", login_btn)

        f = open("answer.txt", 'w')
        for i in range(len(qa_results)):
            print("------------", str(qa_results[i]['title']).strip('?'))
            time.sleep(10)
            start_question_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//a[@class='AskQuestionButton']")))
            driver.execute_script("arguments[0].click();", start_question_btn)

            time.sleep(10)
            question_entry = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='selector_input_interaction'][1]/textarea[@class='selector_input text']")))
            question_entry.send_keys(str(qa_results[i]['title']).strip('?'))

            time.sleep(10)
            add_question_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, "//a[@class='submit_button modal_action' and contains(text(), 'Add Question')]")))
            driver.execute_script("arguments[0].click();", add_question_btn)

            time.sleep(10)
            view_question_btn = WebDriverWait(driver, 50).until(EC.element_to_be_clickable(
                (By.XPATH, "//a[@class='submit_button modal_action' "
                           "and (contains(text(), 'View Question') "
                           "or contains(text(), 'Ask Suggestion') "
                           "or contains(text(), 'View Top Question')) or @role='button']")))
            driver.execute_script("arguments[0].click();", view_question_btn)

            time.sleep(10)
            start_question_btn = WebDriverWait(driver, 50).until(EC.element_to_be_clickable(
                (By.XPATH, "//a[@class='AskQuestionButton']")))
            driver.execute_script("arguments[0].click();", start_question_btn)

            time.sleep(10)
            f.writelines(driver.current_url + '&' + qa_results[i]['answer'] + '\n')

        f.close()

    @staticmethod
    def make_request(url):
        headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36.'
        }
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            return r


if __name__ == "__main__":
    SeleniumBot()
