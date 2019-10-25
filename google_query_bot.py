import time
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

driver = webdriver.Firefox(proxy='163.172.89.109:1369')
driver.get("https://accounts.google.com/signin")

driver.implicitly_wait(3)

driver.find_element_by_id("identifierId").send_keys("please use your email")
driver.find_element_by_id("identifierNext").click()

driver.implicitly_wait(10)
password = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
password.send_keys("please use your email's password")

next_btn = driver.find_element_by_id('passwordNext')
driver.execute_script("arguments[0].click();", next_btn)

time.sleep(80)

driver.get("https://www.google.com/search?authuser=3&q=Tiptop+Restoration+Thousand+Oaks&ludocid=4072880130693755538&lsig=AB86z5XJ6HeUVyZtR9B62-H4vZpH#lpqa=d,3,a,AIe9_BHkHJRvhG8n5BjqdcMSKR_FtZ0igk7RWGmsqq7gCPcPcX7QgGDmnw-7UBfauw03-w2ZniBfbrC4-5ph37CBm-1EURzbFioLCqRT4u3lt-Dtqa8hPGFBGCHDT2oCv6REVH6prbD9")

time.sleep(5)
all_question_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'All questions')]")))
driver.execute_script("arguments[0].click();", all_question_btn)

qa_response = requests.get('https://beta.matrixcore.io/api/panel/seo/qandas/?is_active=1', headers={'accept': 'application/json', 'Authorization': 'Token 4d69c9b7046b12ea7848b8c47be7df4fc2914a30'})
qa_data = qa_response.json()
qa_results = qa_data['results']

user_response = requests.get('https://beta.matrixcore.io/api/panel/seo/accounts/?is_active=1&provider=quora', headers={'accept': 'application/json', 'Authorization': 'Token 4d69c9b7046b12ea7848b8c47be7df4fc2914a30'})
user_data = user_response.json()
user_results = user_data['results']

for i in range(len(qa_results)):
    print("----------------", str(qa_results[i]['title']))
    time.sleep(10)
    ask_question_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ask a question')]")))
    driver.execute_script("arguments[0].click();", ask_question_btn)

    time.sleep(10)
    text_area = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH, "//div[@class='X26Mkf' or @id='pqa_aqr']/textarea")))
    text_area.send_keys(qa_results[i]['title'])

    time.sleep(10)
    post_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'POST')]")))
    driver.execute_script("arguments[0].click();", post_btn)

    time.sleep(10)
    ask_another_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//g-flat-button[contains(text(), 'Ask another')]")))
    driver.execute_script("arguments[0].click();", ask_another_btn)


