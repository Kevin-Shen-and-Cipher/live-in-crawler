from apartment.apartment_crawler import ApartmentCrawler
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json


class Apartment591Carwler(ApartmentCrawler):
    def __init__(self) -> None:
        super().__init__()

    def get_web_data(self, chrome):
        result = 0

        return result
