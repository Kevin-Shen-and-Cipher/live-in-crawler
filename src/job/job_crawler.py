from abc import ABC, abstractmethod
from webbrowser import Chrome
from dotenv import load_dotenv
from src.crawler.Crawler import Crawler
import json
import requests
import re
import os

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
            if i["fields"]["name"].find(district) > -1:
                return i["pk"]
        return None
    
    def get_salary(self,salary):
        s1 = re.findall(r'\d+', salary)
        s2=int(s1[0]+"0000")
        return s2
    
    def working_hour(self,work):
        with open("src/job/job_data/working_hour.json",encoding="utf-8") as file:
            data=json.load(file)
        for i in data:
            if work.find(i["fields"]["name"]) >= 0:
                return i["pk"]
        return None
    
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

    def post_data(self, data):
        load_dotenv(".env")
        url = os.getenv("JOBS_URL")
        return requests.post(url=url, headers={'Content-type': 'application/json'}, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def post_error(self, response, data_number):
        f = open(("error_log/error_status_%s.html"% (data_number)), "w", encoding="utf-8")
        f.write(response)
        f.close()