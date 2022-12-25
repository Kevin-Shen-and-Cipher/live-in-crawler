from job.job_crawler import JobCrawler
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json


class Job104Carwler(JobCrawler):
    def __init__(self) -> None:
        super().__init__()

    def get_web_data(self, chrome):
        result = 0
        return result
    
    def get_dirstrict(self, district):
        with open("src/apartment/apartment_data/district.json", encoding="utf-8") as file:
            district_data = json.load(file)
        for i in district_data:
            if i["fields"]["name"] == district:
                return i["pk"]
        return None