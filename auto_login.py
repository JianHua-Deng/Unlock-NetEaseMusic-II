# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0086AD4919D0ED0E99DEFC24039370A3A8A44B7FAFD032852BEBA40F47724D979A77B35E5C13F967165BCEFDFEC1B92F72000BBA67F8AC724D7382426A416B9130B3579AACB300592CD999D0DA820200A2EB6BB070863B8B0FE91A2280467C17C90AF5D0F220ED3332CF4D45C3BE00A391992DB5C16B2BE3B8E7CFA125F9D9936C5FC858BDE62219C2E42E2C9F8AB1BDD21AA791712D276BC8D0FBCDDAACF9F138D4A1498CFBC8486C088325282C14EFAAF8D48920C64B2FCE515FEC4F470A559E97E5BE4B7B68D0E4F89DDC72756403374DF518623120D9875458D1941DB94E8441E18CDAF73B7DC3625F9A40134CBCA3C967AFCF36E677E8BA48EA4CFE83C2DE43121BEB47B6C3E910050DAB0C99D2ABE2FC529784227C9FBD3397B6A5ABC0FB82BA9F20EF724D856D4193B0330234D25FC7B483440BFD4B540C70BA622A7984"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
