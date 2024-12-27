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
        print(job)
        with open("src/job/job_data/job_position.json",encoding="utf-8") as file:
            job_data=json.load(file)
        for i in job_data:
            if i["fields"]["name"] in job:
                return i["pk"]
        return None        
    
    def get_dirstrict(self, district):
        with open("src/apartment/apartment_data/district.json", encoding="utf-8") as file:
            district_data = json.load(file)
        for i in district_data:
            if i["fields"]["name"].find(district) > -1:
                return i["pk"]
        return None
    
    # 只回傳薪水
    def get_salary(self,salary):

        if "以上" in salary:
            return 40000
        print(salary)
        if "月薪" in salary: 
            return int(salary[4:10].replace(",", ""))
        return None 
        if salary.find("月薪") > -1:
            if salary.find("萬") > -1:
                job_salary = re.findall(r'\d+\.?\d*', salary.split("萬")[0])[0]
                try:
                    if job_salary.find(".") > -1:
                        job_salary = job_salary.replace(".", "")
                        job_salary = int(job_salary + "000")
                    else:
                        job_salary = int(job_salary + "0000")
                    if job_salary != 0:
                        return job_salary
                except Exception as e:
                    print(e)
                    return None
        return None
    
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
        load_dotenv(".env", override=True)
        url = os.getenv("JOBS_URL")
        print(url)
        # print(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        return requests.post(url=url, headers={'Content-type': 'application/json'}, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def post_error(self, response, data_number):
        f = open(("error_log/error_status.txt"), "a", encoding="utf-8")
        f.write("\ndata_number {} : ".format(data_number))
        f.write(response)
        f.close()