from .job_crawler import JobCrawler
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import traceback
import json



class job_1111_cwler(JobCrawler):
    def __init__(self):
        self.region = [100,200]
        super().__init__()
    
    def get_dirstrict(self, district):
        district =district.split("區",1)[0]
        return super().get_dirstrict(district)
    
    def job_link(self):
        try:
            for i in self.region:
                data_count =0
                page_row =0
            while data_count <self.data_limit:
                
                region_url="https://www.1111.com.tw/search/job?c0=100%s&d0=140802%2C140803%2C140202&page=%s"%(str(i),str(page_row))
                self.get_web(region_url)
                if self.wait_element(By.CLASS_NAME,"item__job"):
                    print("Can not connect to the page %s, please check the internet status or 591 connection block" % (region_url))
                    exit(0)
                page_element = BeautifulSoup(self.browser.page_source, "html.parser")
                rent_list = page_element.find_all("section", {"class": "item__job"})
                for rent_item in rent_list:
                    if data_count >=self.data_limit:
                        break
                    web_data = self.get_web_data(rent_item.find("a", href=True)["href"])
                    if web_data != None:
                        result=self.post_data(web_data)
                        if result.status_code != 201:
                            self.post_error(result.text,web_data["url"].split("/job/")[1])
                            print("web data error" + web_data ["url"])
                            continue
                        else:
                            print(result)
                        data_count +=1
                    else:
                        print("data error %s" % rent_item.find("a", href=True)["href"])
            page_row +=30
        except Exception as e:
            print("eeeee")
            self.browser.quit()
        

            
        
    def get_job_data(self,job_url:str):
        try:
            data={}
            data["url"]=job_url
            if self.wait_element(By.CLASS_NAME, "col-sm-8"):
                print("page %s not found!" % (data["url"]))
                return None
            address=self.browser.find_elements(By.CLASS_NAME,"align-items-top")
            data["name"]=self.browser.find_element(By.CLASS_NAME,"title_4").text
            print(data["name"])
            data["salary"]=self.get_salary((self.browser.find_element(By.CLASS_NAME,"job_salary").text))
            
            data["tenure"]=self.browser.find_element(By.CLASS_NAME,"data_trans").find_element(By.CLASS_NAME,"applicants").text.replace("\n",'')[4:]
            
            data["address"]=address[4].find_element(By.CLASS_NAME,"job_info_content").text
            
            data["URL"]=self.brower.find_element(By.NAME,"twitter:url").get_attribute('Content')
            
            data["district"]=(self.get_dirstrict(data["address"]))
            
            data["job_position"]=self.get_job_position(self.get_job_position(address[3].text.replace('\n','')[5:]))
            
            #work_hour
            data["work_hour"]=self.get_work_hour((address[0]).text.replace('\n'," "))
            
            #benfit
            benefitlist=self.browser.find_elements(By.CLASS_NAME,"job_benefits")
            try:
                b1=benefitlist[0].find_element(By.CLASS_NAME,"job_benefits_items").find_element(By.CLASS_NAME,"body_2").text.split('、')
            except:
                b1=benefitlist[0].find_element(By.CLASS_NAME,"job_benefits_items").find_element(By.CLASS_NAME,"body_2").text
            try:
                b2=benefitlist[1].find_element(By.CLASS_NAME,"job_benefits_items").find_element(By.CLASS_NAME,"body_2").text.split('、')
            except:
                b2=benefitlist[1].find_element(By.CLASS_NAME,"job_benefits_items").find_element(By.CLASS_NAME,"body_2").text
                b1+=b2
            data["benefit"]=b1
            
        except:
            traceback.print_exc()
            self.browser.quit()
        return None
            