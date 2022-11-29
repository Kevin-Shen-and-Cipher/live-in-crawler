from .apartment_crawler import ApartmentCrawler
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import traceback
import json


class Apartment591Carwler(ApartmentCrawler):
    def __init__(self) -> None:
        self.region = [1, 3]
        super().__init__()

    def get_dirstrict(self, district):
        district = district.split("區",1)[0] + "區" 
        print(district)
        return super().get_dirstrict(district)

    def coordinate_to_DD(self, coordinate:str):
        print(coordinate)
        coord = coordinate.split(" ")
        coordinate = "N%s E%s" % (str(int(coord[0].split("°")[0])+int(coord[0].split("°")[1].split("'")[0])/60+int(coord[0].split("°")[1].split("'")[1].split("\"")[0])/3600), str(int(coord[1].split("°")[0])+int(coord[1].split("°")[1].split("'")[0])/60+int(coord[1].split("°")[1].split("'")[1].split("\"")[0])/3600))
        print(coordinate)
        exit(0)
        return coordinate 

    def get_web_data(self):
        try:
            for i in self.region:
                page_row = 0
                while page_row <= 60:
                    region_url = "https://rent.591.com.tw/?region=%s&firstRow=%s" % (str(i), str(page_row))
                    self.get_web(url=region_url)
                    # 等待租房列表讀取完成
                    if self.wait_element(By.CLASS_NAME, "vue-list-rent-item"):
                        continue
                    # 把讀取完成的列表透過beautifulSoup轉為一般的文字檔 如果用 selenium 會需要在該頁面讀取到元素才可以調用
                    page_element = BeautifulSoup(self.browser.page_source, "html.parser")
                    rent_list = page_element.find_all("section", {"class": "vue-list-rent-item"})
                    # 開始對讀取每個租屋資料
                    for rent_item in rent_list:
                        data = {}
                        data["url"] = rent_item.find("a", href=True)["href"]
                        self.get_web(data["url"])
                        if self.wait_element(By.XPATH, "//section[@id='surround-map']"):
                            continue
                        house_content = self.browser.find_element(By.CLASS_NAME, "left-con")
                        house_info = house_content.find_element(By.XPATH, "//section[@class='house-info']")
                        data["name"] = house_info.find_element(By.XPATH, "//div[@class='house-title']//h1").text
                        data["price"] = house_info.find_element(By.XPATH, "//div[@class='house-price']//span[@class='price']//b").text
                        data["address"] = house_content.find_element(By.CLASS_NAME, "load-map").text
                        data["coordinate"] = house_content.find_element(By.CSS_SELECTOR, "div.lat-lng").get_attribute("innerHTML").replace("\'", "'")
                        data["coordinate"] = self.coordinate_to_DD(data["coordinate"])
                        data["dirstrict"] = self.get_dirstrict(data["address"])
                        print(data)
                    page_row += 30
            self.browser.quit()
        except:
            traceback.print_exc()
            self.browser.quit()
