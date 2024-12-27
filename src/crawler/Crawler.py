import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Crawler(object):
    def __init__(self):
        options = self.set_option()
<<<<<<< HEAD
        self.browser = webdriver.Chrome(options=options)
        self.data_limit = 2
=======
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.data_limit = 10
>>>>>>> 035a56d (fix: crawler)
        self.data = []

    def set_option(self):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--user-agent=%s" % user_agent)
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        return options

    def wait_element(self, by_element, element, sec=5) -> bool:
        try:
            WebDriverWait(self.browser, sec).until(
                EC.presence_of_element_located((by_element, element))
            )
            return False
        except Exception as e:
            return True

    def page_source(self):
        return self.browser.page_source

    def get_web(self, url):
        return self.browser.get(url)

    def check_data(self, data: dict) -> bool:
        data_error = False
        for i in data.keys():
            if data[i] == None:
                # print("%s data is missing" % (i))
                data_error = True
        if data_error:
            return True
        else:
            return False
