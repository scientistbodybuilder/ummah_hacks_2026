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
    'https://aaoifi.com/ss-2-debit-card-charge-card-and-credit-card/?lang=en',
    'https://aaoifi.com/ss-3-procrastinating-debtor/?lang=en',
    'https://aaoifi.com/ss-4-settlement-of-debt-by-set-off/?lang=en',
    'https://aaoifi.com/ss-5-guarantees/?lang=en',
    'https://aaoifi.com/ss-6-conversion-of-a-conventional-bank-to-an-islamic-bank/?lang=en',
    'https://aaoifi.com/ss-7-hawalah/?lang=en',
    'https://aaoifi.com/ss-8-murabahah/?lang=en',
    'https://aaoifi.com/ss-9-ijarah-and-ijarah-muntahia-bittamleek/?lang=en',
    'https://aaoifi.com/ss-10-salam-and-parallel-salam/?lang=en',
    'https://aaoifi.com/ss-11-istisnaa-and-parallel-istisnaa/?lang=en',
    'https://aaoifi.com/ss-12-sharikah-musharakah-and-modern-corporations/?lang=en',
    'https://aaoifi.com/s-13-mudarabah/?lang=en',
    'https://aaoifi.com/ss-14-documentary-credit/?lang=en',
    'https://aaoifi.com/ss-15-jualah/?lang=en',
    'https://aaoifi.com/ss-16-commercial-papers/?lang=en',
    'https://aaoifi.com/ss-17-investment-sukuk/?lang=en',
    'https://aaoifi.com/ss-18-possession-qabd/?lang=en',
    'https://aaoifi.com/ss-19-loan-qard/?lang=en',
    'https://aaoifi.com/ss-20-sale-of-commodities-in-organized-markets/?lang=en',
    'https://aaoifi.com/ss-21-financial-paper-shares-and-bonds/?lang=en',
    'https://aaoifi.com/ss-22-concession-contracts/?lang=en',
    'https://aaoifi.com/ss-23-agency-and-the-act-of-an-uncommissioned-agent-fodooli/?lang=en',
    'https://aaoifi.com/ss-24-syndicated-financing/?lang=en',
    'https://aaoifi.com/ss-25-combination-of-contracts/?lang=en',
    'https://aaoifi.com/ss-26-islamic-insurance/?lang=en',
    'https://aaoifi.com/ss-27-indices/?lang=en',
    'https://aaoifi.com/ss-28-banking-services-in-islamic-banks/?lang=en',
    'https://aaoifi.com/ss-29-stipulations-and-ethics-of-fatwa-in-the-institutional-framework/?lang=en',
    'https://aaoifi.com/ss-30-monetization-tawarruq/?lang=en',
    'https://aaoifi.com/ss-31-controls-on-gharar-in-financial-transactions/?lang=en',
    'https://aaoifi.com/ss-32-arbitration/?lang=en',
    'https://aaoifi.com/ss-33-waqf/?lang=en',
    'https://aaoifi.com/ss-34-hiring-of-persons/?lang=en',
    'https://aaoifi.com/ss-35-zakah/?lang=en',
    'https://aaoifi.com/ss-36-impact-of-contingent-incidents-on-commitments/?lang=en',
    'https://aaoifi.com/ss-37-credit-agreement/?lang=en',
    'https://aaoifi.com/ss-38-online-financial-dealings/?lang=en',
    'https://aaoifi.com/ss-39-mortgage-and-its-contemporary-applications/?lang=en',
    'https://aaoifi.com/ss-40-distribution-of-profit-in-mudarabah-based-investment-accounts/?lang=en',
    'https://aaoifi.com/ss-41-islamic-reinsurance/?lang=en',
    'https://aaoifi.com/ss-42-financial-rights-and-how-they-are-exercised-and-transferred/?lang=en',
    'https://aaoifi.com/ss-43-insolvency/?lang=en',
    'https://aaoifi.com/ss-44-obtaining-and-deploying-liquidity/?lang=en',
    'https://aaoifi.com/ss-45-protection-of-capital-and-investments/?lang=en',
    'https://aaoifi.com/ss-46-al-wakalah-bi-al-istithmar-investment-agency/?lang=en',
    'https://aaoifi.com/ss-47-rules-for-calculating-profit-in-financial-transactions/?lang=en',
    'https://aaoifi.com/ss-48-options-to-terminate-due-to-breach-of-trust-trust-based-options/?lang=en',
    'https://aaoifi.com/ss-49-unilateral-and-bilateral-promise/?lang=en',
    'https://aaoifi.com/ss-50-irrigation-partnership-musaqat/?lang=en',
    'https://aaoifi.com/ss-51-options-to-revoke-contracts-due-to-incomplete-performance/?lang=en',
    'https://aaoifi.com/ss-52-options-to-reconsider/?lang=en',
    'https://aaoifi.com/ss-53-arboun-earnest-money/?lang=en',
    'https://aaoifi.com/ss-54-revocation-of-contracts-by-exercise-of-a-cooling-off-option/?lang=en',
    'https://aaoifi.com/ss-55-competitions-and-prizes/?lang=en',
    'https://aaoifi.com/ss-57-the-gold-standard/?lang=en',
    'https://aaoifi.com/themencode-pdf-viewer-sc/?lang=en&tnc_pvfw=ZmlsZT1odHRwczovL2Fhb2lmaS5jb20vd3AtY29udGVudC91cGxvYWRzLzIwMjUvMDUvQUFPSUZJLVNTLi01OS1TYWxlLW9mLURlYnQtRW5nLi5wZGYmc2V0dGluZ3M9MDAxMDAwMTExMDAwMDAwMTEwMCZsYW5nPWVuLVVT#page=&zoom=&pagemode=none',
    'https://aaoifi.com/themencode-pdf-viewer-sc/?lang=en&tnc_pvfw=ZmlsZT1odHRwczovL2Fhb2lmaS5jb20vd3AtY29udGVudC91cGxvYWRzLzIwMjUvMDUvQUFPSUZJLVNTLi02MC1XYXFmLUVuZ2xpc2gucGRmJnNldHRpbmdzPTAwMTAwMDExMTAwMDAwMDExMDAmbGFuZz1lbi1VUw==#page=&zoom=&pagemode=none'
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
    tm.sleep(5)
    iframe = driver.find_element(By.CSS_SELECTOR, "iframe")
    driver.switch_to.frame(iframe)

    # total_pages_element  = WebDriverWait(driver,timeout).until(EC.presence_of_element_located((By.ID, "numPages")))
    # total_pages = int(re.sub(r"\D", "", total_pages_element.text))
    # print("total pages: ",total_pages)
    # frame = WebDriverWait(driver, timeout).until(
    # EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe"))
    # )
    total_pages_element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "numPages"))
    )
    total_pages = int(re.sub(r"\D", "", total_pages_element.text))
    print("total pages: ",total_pages)

    for i in range(total_pages):
        # switch back into the iframe
        print(f"current page: {i+1}")
        # iframe = driver.find_element(By.CSS_SELECTOR, "iframe[width='1000'][height='1000']")
        # driver.switch_to.frame(iframe)
        # scroll to that page
        element = WebDriverWait(driver,timeout).until(EC.presence_of_element_located((By.XPATH, f"//div[@class='page' and @data-page-number='{i+1}']")))
        driver.execute_script("arguments[0].scrollIntoView();", element)

        # parse text
        try:
            span_list = WebDriverWait(driver,timeout).until(EC.presence_of_all_elements_located((By.XPATH, f"//div[@class='page' and @data-page-number='{i+1}']/div[@class='textLayer']/span")))
            len_lines = len(span_list)
            for j in range(len_lines):
                lines = WebDriverWait(driver,timeout).until(EC.presence_of_all_elements_located((By.XPATH, f"//div[@class='page' and @data-page-number='{i+1}']/div[@class='textLayer']/span")))

                parsed_text = lines[j].text
                content.append(parsed_text)
                print("scraped this text: ", parsed_text)

        except Exception as e:
            pass
               
                    

        # move to the next page
        # try:
        #     next_button = WebDriverWait(driver,timeout).until(EC.presence_of_element_located((By.ID, "pvfw-next-page")))
        #     next_button.click()
        # except Exception as e:
        #     # we are at the last page
        #     pass
        # combine content into one large markdown file
        print(f"content from page {i+1}: ",content)

    markdown = "\n".join(content)

    with open(f"{title}.md", "w", encoding="utf-8") as f:
        f.write(markdown)

















print('quit driver')
driver.quit()   

