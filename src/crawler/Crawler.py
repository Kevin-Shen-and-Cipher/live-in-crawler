from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Crawler(object):

    def __init__(self):
        options = self.set_option()
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.data = []

    def set_option(self):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument('--user-agent=%s' % user_agent)
        # disable gpu to show web 
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        
        return options

    def wait_element(self, by_element, element, sec=10) -> bool: 
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
