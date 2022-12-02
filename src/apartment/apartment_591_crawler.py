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
        return super().get_dirstrict(district)

    def get_web_url(self):
        try:
            for i in self.region:
                page_row = 0
                data_count = 0
                while data_count <= self.data_limit:
                    region_url = "https://rent.591.com.tw/?region=%s&firstRow=%s" % (str(i), str(page_row))
                    self.get_web(url=region_url)
                    # 等待租房列表讀取完成
                    if self.wait_element(By.CLASS_NAME, "vue-list-rent-item"):
                        print("Can not connect to the page %s, please check the internet status or 591 connection block" % (region_url))
                        exit(0)
                    page_element = BeautifulSoup(self.browser.page_source, "html.parser")
                    rent_list = page_element.find_all("section", {"class": "vue-list-rent-item"})
                    for rent_item in rent_list:
                        if data_count >= self.data_limit:
                            break
                        web_data = self.get_web_data(rent_item.find("a", href=True)["href"])
                        if web_data != None:
                            self.post_data(web_data)
                            data_count += 1
                        else:
                            print("data error %s" % rent_item.find("a", href=True)["href"])
                            continue
                    page_row += 30
        except:
            self.browser.quit()

    def get_web_data(self, rent_url:str):
        try:
            data = {}
            data["url"] = rent_url
            self.get_web(data["url"])
            if self.wait_element(By.XPATH, "//section[@id='surround-map']"):
                print("page %s not found!" % (data["url"]))
                return None
            house_content = self.browser.find_element(By.CLASS_NAME, "left-con")
            house_info = house_content.find_element(By.XPATH, "//section[@class='house-info']")
            data["name"] = house_info.find_element(By.XPATH, "//div[@class='house-title']//h1").text
            data["price"] = house_info.find_element(By.XPATH, "//div[@class='house-price']//span[@class='price']//b").text
            data["address"] = house_content.find_element(By.CLASS_NAME, "load-map").text
            data["dirstrict"] = self.get_dirstrict(data["address"])
            data["coordinate"] = self.DMS_to_DD(house_content.find_element(By.CSS_SELECTOR, "div.lat-lng").get_attribute("innerHTML").replace("\'", "'"))
            
            #house pattern section 
            house_pattern = house_info.find_element(By.CLASS_NAME, "house-pattern").find_elements(By.TAG_NAME, "span")
            data["rent_type"] = self.get_rent_type(house_pattern[0].text)
            data["aparment_type"] = self.get_aparment_type(house_pattern[len(house_pattern)-1].text)
            data["room_type"] = self.get_room_type(house_pattern)
            
            #get restrict section
            try:
                data["restrict"] = self.get_restrict(house_content.find_element(By.CLASS_NAME, "service-rule").find_element(By.TAG_NAME, "span").text)
            except Exception as e:
                data["restrict"] = [1]
            
            #get device section
            try:
                data["device"] = self.get_device(house_content.find_element(By.CLASS_NAME, "service-list-box").find_elements(By.CLASS_NAME, "service-list-item"))
            except Exception as e:
                #self.browser.execute_script("window.open('%s');" % (data["url"]))
                data["device"] = [1]
            
            #get facility section
            data["surrounding_facility"] = self.get_facility_type(self.browser.find_element(By.ID, "surround-map").find_elements(By.CLASS_NAME, "result-list-item"))
            # check data error sectio
            if self.check_data(data):
                return None
            else:
                return data
        except:
            traceback.print_exc()
            self.browser.quit()
        return None
