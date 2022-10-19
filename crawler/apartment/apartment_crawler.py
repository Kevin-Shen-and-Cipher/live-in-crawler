from abc import ABC, abstractmethod
from webbrowser import Chrome
from apartment.apartment_sql import ApartmentSql
from crawler.crawler import Crawler


class ApartmentCrawler(ABC, Crawler):

    def get_apartment(self):
        chrome = self.get_chrome(self)

        #獲取網頁內容
        data = self.get_web_data(chrome)

        # 新增租屋資料
        sql = ApartmentSql()
        sql.add(data)

        chrome.close()

    @abstractmethod
    def get_web_data(self, chrome: Chrome):
        return NotImplemented
