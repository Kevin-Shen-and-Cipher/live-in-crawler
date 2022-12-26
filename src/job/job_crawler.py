from abc import ABC, abstractmethod
from webbrowser import Chrome
from src.crawler.Crawler import Crawler
import json
import re

class job_crawler(ABC, Crawler):

    def __init__(self) -> None:
        super().__init__()
        self.data_limit= 90
    
    def job_position(self,job: str):
        with open("src/job/job_data/job_position.json",encoding="utf-8") as file:
            job_data=json.load(file)
        for i in job_data:
            if i["fields"]["name"]==job:
                return i["pk"]
        return None        
    
    def get_dirstrict(self, district):
        with open("src/apartment/apartment_data/district.json", encoding="utf-8") as file:
            district_data = json.load(file)
        for i in district_data:
            if district.find(i["fields"]["name"]) >= -1:
                return i["pk"]
        return None
    
    def get_salary(self,salary):
        s1 = re.findall(r'\d+', salary)
        s2=int(s1[0]+"0000")
        return s2
    
    def working_hour(self,work):
        with open("src/job/job_data/working_hour.json",encoding="utf-8") as file:
            data=json.load(file)
        return_data = []
        for i in data:
            if work.find(i["fields"]["name"]) >= 0:
                return_data.append(i["pk"])
        return return_data if return_data != [] else None
    
    def get_position(self,position):
        with open("src/job/job_data/job_position.json",encoding="utf-8")as file:
            data=json.lod(file)
        try:
            position=position.split('、')
        except:
            position   
        for i in data:
            if  i["fields"]["name"] == position:
                return i["pk"]
        return None