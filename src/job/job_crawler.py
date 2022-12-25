from abc import ABC, abstractmethod
from webbrowser import Chrome
from ..crawler import Crawler
from job.job_sql import JobSql
import json
import re

class JobCrawler(ABC, Crawler):

    def __init__(self) -> None:
        super().__init__()
        self.data_limit= 90
    
    def job_position(self,job):
        with open("C:\Users\bernie\Desktop\test_git\live-in-crawler\src\job\job_data\job_position.json",encoding="utf-8") as file:
            job_data=json.load(file)
        for i in job_data:
            if i["fields"]["name"]==job:
                return i["pk"]
        return None        
    
    def get_dirstrict(self, district):
        with open("src/apartment/apartment_data/district.json", encoding="utf-8") as file:
            district_data = json.load(file)
        for i in district_data:
            if i["fields"]["name"] ==district:
                return i["pk"]
    
    def get_salary(self,salary):
            s1 = re.findall(r'\d+', salary)
            s2=int(s1[0]+"0000")
            return s2
    
    def working_hour(self,work):
        with open("C:\Users\bernie\Desktop\test_git\live-in-crawler\src\job\job_data\working_hour.json",encoding="utf-8") as file:
            data=json.load(file)
        try:
            time2=(((work[:work.index("　說明")])[6:]).split("、"))
        except:
            time2=work[5:]
        for i in data:
            if  i["fields"]["name"] == work:
                return i["pk"]
        return None
    
    def get_position(self,position):
        with open("C:\Users\bernie\Desktop\test_git\live-in-crawler\src\job\job_data\job_position.json",encoding="utf-8")as file:
            data=json.lod(file)
        try:
            position=position.split('、')
        except:
            position   
        for i in data:
            if  i["fields"]["name"] == position:
                return i["pk"]
        return None
    
    def get_jobs(self):
        chrome = self.get_chrome(self)

        #獲取網頁內容
        data = self.get_web_data(chrome)

        # 新增工作資料
        sql = JobSql()
        sql.add(data)

        chrome.close()

    @abstractmethod
    def get_web_data(self, chrome: Chrome):
        return NotImplemented
