import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Crawler(object):

    def get_chrome(self):
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=self.__get_options())

    def __get_options():
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1420,1080')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        return options

    def is_element_appeared(chrome: Chrome, By: By, elementName: string):
        return WebDriverWait(chrome, 10).until(
            EC.presence_of_element_located((By, elementName)))
