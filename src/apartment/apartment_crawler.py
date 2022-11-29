from abc import ABC, abstractmethod
from dotenv import load_dotenv
from src.crawler.Crawler import Crawler
import json
import os

class ApartmentCrawler(ABC, Crawler):

    def get_dirstrict(self, district):
        with open("default_data/district.json", encoding="utf-8") as file:
            district_data = json.load(file)
        for i in district_data:
            if i["fields"]["name"] == district:
                return i["pk"]
    
    def get_rent_type(self, rent_type):
        with open("default_data/district.json", encoding="utf-8") as file:
            data = json.load(file)
        for i in data:
            if  i["fields"]["name"] == rent_type:
                return i["pk"]

    def add_data(self, data):
        self.data.append(data)

    def post_data(self):
        load_dotenv()
        url = os.getenv("APARMENTS_URL")
        print(url)
