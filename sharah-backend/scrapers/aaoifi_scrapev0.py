from datetime import datetime, timezone
from flask import Flask, request, jsonify
from selenium import webdriver
import re, io
import requests

# db
# from flask_sqlalchemy import SQLAlchemy
# scrap
from flask_cors import CORS
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time as tm, os, subprocess
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException, ElementNotInteractableException


urls = [
    'https://aaoifi.com/ss-1-trading-in-currencies/?lang=en',
    # 'https://aaoifi.com/ss-2-debit-card-charge-card-and-credit-card/?lang=en',
    # 'https://aaoifi.com/ss-3-procrastinating-debtor/?lang=en',
    # 'https://aaoifi.com/ss-4-settlement-of-debt-by-set-off/?lang=en',
    # 'https://aaoifi.com/ss-5-guarantees/?lang=en',
    # 'https://aaoifi.com/ss-6-conversion-of-a-conventional-bank-to-an-islamic-bank/?lang=en',
    # ''
]

service = Service(ChromeDriverManager().install())
options = Options()
#options.add_argument(f'--proxy-server=={}')
# options.add_argument(r'--user-data-dir=C:\Users\ser\AppData\Local\Google\Chrome\User Data\Default')
options.add_argument("--window-size=2560,1600")
options.add_argument('--log-level=1')
options.add_argument("--headerless=new")
options.add_argument("--disable-background-networking")
options.add_argument("--disable-background-timer-throttling")
options.add_argument("--disable-backgrounding-occluded-windows")
options.add_argument("--disable-sync")
options.add_argument("--disable-features=TranslateUI")
options.add_argument("--disable-ipc-flooding-protection")
options.add_argument("--no-first-run")
options.add_argument("--no-service-autorun")
driver = webdriver.Chrome(service=service, options=options)
timeout = 30

for url in urls:
    print('scraping: ',url)
    driver.get(url)

    title_element = WebDriverWait(driver,timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@class='row about']/div/div/h2")))
    title = title_element.text
    print("title: ",title)
    content = []
    # Get body text
    # page_list = WebDriverWait(driver,timeout).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='pdfViewer']/div")))
    # page_list = WebDriverWait(driver,timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@class='pdfViewer']/div")))
    # page_count = len(page_list)
    # print(f"there are {page_count} pages")
    total_pages_element  = WebDriverWait(driver,timeout).until(EC.presence_of_element_located((By.ID, "numPages")))
    total_pages = int(re.sub(r"\D", "", total_pages_element.text))
    for i in range(total_pages):
        print(f"current page: {i+1}")
        # scroll to that page
        element = WebDriverWait(driver,timeout).until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'page') and @data-page-number='{i+1}']")))
        driver.execute_script("arguments[0].scrollIntoView();", element)

        # parse text
        span_list = WebDriverWait(driver,timeout).until(EC.presence_of_all_elements_located((By.XPATH, f"//div[contains(@class, 'page') and @data-page-number='{i+1}']/div[contains(@class, 'textLayer')]/span")))
        len_lines = len(span_list)
        for j in range(len_lines):
            lines = WebDriverWait(driver,timeout).until(EC.presence_of_all_elements_located((By.XPATH, f"//div[contains(@class, 'page') and @data-page-number='{i+1}']/div[contains(@class, 'textLayer')]/span")))

            try:
                parsed_text = lines[j].text


            except StaleElementReferenceException as e:
                tm.sleep(2)
                parsed_text = lines[j].text
            finally:
                content.append(parsed_text)
                print("scraped this text: ", parsed_text)

        # move to the next page
        try:
            next_button = WebDriverWait(driver,timeout).until(EC.presence_of_element_located((By.ID, "pvfw-next-page")))
            next_button.click()
        except Exception as e:
            # we are at the last page
            pass
        # combine content into one large markdown file
        print("content: ",content)

















print('quit driver')
driver.quit()   

