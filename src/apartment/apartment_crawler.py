from abc import ABC
from dotenv import load_dotenv
from src.crawler.Crawler import Crawler
import json
import os

class ApartmentCrawler(ABC, Crawler):
    
    def DMS_to_DD(self, DMS:str):
        coord = DMS.split(" ")
        DMS = "N%s E%s" % (str(int(coord[0].split("°")[0])+int(coord[0].split("°")[1].split("'")[0])/60+int(coord[0].split("°")[1].split("'")[1].split("\"")[0])/3600), str(int(coord[1].split("°")[0])+int(coord[1].split("°")[1].split("'")[0])/60+int(coord[1].split("°")[1].split("'")[1].split("\"")[0])/3600))
        return DMS 
    
    def get_dirstrict(self, district):
        with open("/apartment_data/district.json", encoding="utf-8") as file:
            district_data = json.load(file)
        for i in district_data:
            if i["fields"]["name"] == district:
                return i["pk"]
    
    def get_rent_type(self, rent_type: str):
        with open("default_data/rent_type.json", encoding="utf-8") as file:
            data = json.load(file)
        if ((rent_type.find("廳") != -1) and (rent_type.find("衛") != -1)) == True:
            rent_type = "整層住家"
        for i in data:
            if  i["fields"]["name"] == rent_type:
                return i["pk"]
        return None
    
    def get_aparment_type(self, aparment_type: str):
        with open("/apartment_data/apartment_type.json", encoding= "utf-8") as file:
            data = json.load(file)
        for i in data:
            if aparment_type.find(i["fields"]["name"]) != -1:
                return i["pk"]
        return None
        
    def get_facility_type(self, element):
        with open("/apartment_data/facility_type.json") as file:
            data = json.load(file)
        return_data = []
        traffic = element[0].find_element(By.CLASS_NAME, "traffic").find_elements(By.TAG_NAME, "dl")
        school = element[2].find_elements(By.CLASS_NAME, "name")
        for i in traffic:
            facility_type = 0
            for model in data:
                if i.find_element(By.TAG_NAME, "dt").get_attribute("textContent").find(model["fields"]["name"]) != -1:
                    facility_type = model["pk"]
            for k in i.find_elements(By.CLASS_NAME, "name"):
                return_data.append({"name": k.get_attribute("textContent").replace(" ", "").replace("\n", ""), "facility_type":facility_type})
        for i in school:
            facility_type = 0
            for model in data:
                if model["fields"]["name"].find("學校"):
                    facility_type = model["pk"]
            return_data.append({"name": i.get_attribute("textContent").replace(" ", "").replace("\n", ""), "facility_type":facility_type})
        if len(return_data) == 0:
            return None
        else:
            return return_data
    
    def get_room_type(self, room_type_list: str):
        with open("/apartment_data/room_type.json", encoding= "utf-8") as file:
            data = json.load(file)
        for element_data in room_type_list:
            element_text = element_data.text
            if element_text.find("衛") != -1 and element_text.find("廳") != -1: 
                index = element_text.find("房")
                room_count = element_text[index-1:index]
                for i in data:
                    if int(i["fields"]["name"][0:1]) >= int(room_count):
                        return i["pk"]
                return None
            else:
                continue
        return [1]
    
    def get_restrict(self, service_line: str):
        with open("/apartment_data/restrict.json", encoding="utf-8") as file:
            data = json.load(file)
        return_data = []
        for i in data:
            if service_line.find(i["fields"]["name"]) != -1:
                return_data.append(i["pk"])
        if len(return_data) != 0:
            return return_data
        else:
            return [1]
    
    def get_device(self, device_list: list):
        with open("/apartment_data/device.json", encoding="utf-8") as file:
            data = json.load(file)
        return_data = []
        for i in device_list:
            if i.get_attribute("class") == "service-list-item":
                item_text = i.find_element(By.CLASS_NAME, "text").text
                for k in data:
                    if item_text.find(k["fields"]["name"]) != -1:
                        return_data.append(k["pk"])
        if len(return_data) != 0:
            return return_data
        else:
            return [1]
    
    def post_data(self):
        load_dotenv()
        url = os.getenv("APARMENTS_URL")
        print(url)
