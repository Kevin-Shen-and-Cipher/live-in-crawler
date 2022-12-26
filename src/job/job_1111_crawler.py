from src.job.job_crawler import job_crawler
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import traceback
import time
import json



class job_1111_crawler(job_crawler):
    def __init__(self):
        self.region = [100,200]
        super().__init__()
    
    def get_dirstrict(self, district):
        district =district.split("區",1)[0]
        return super().get_dirstrict(district)
    
    def job_link(self):
        for i in self.region:
            data_count = 0
            page_row = 1
            data_b = 1
            while data_count < self.data_limit:
                try:
                    region_url=("https://www.1111.com.tw/search/job?c0=100{}&d0=140802%2C140803%2C140202&page={}").format(str(i), str(page_row))
                    self.get_web(region_url)
                    if self.wait_element(By.CLASS_NAME,"job-list-item"):
                        print("Can not connect to the page %s, please check the internet status or 591 connection block" % (region_url))
                        exit(0)
                    page_element = BeautifulSoup(self.browser.page_source, "html.parser")
                    rent_list = page_element.find("div", {"data-b": data_b})
                    rent_list = rent_list.find_all("div", {"class": "job_item_info"})                 
                    for job_item in rent_list:
                        print(self.get_web_data(job_item.find_all("a", href=True)[0]["href"]))
                    #for rent_item in rent_list:
                    #    if data_count >=self.data_limit:
                    #        break
                    #    web_data = self.get_web_data(rent_item.find("a", href=True)["href"])
                    #    print(web_data)
                        # if web_data != None:
                        #     result=self.post_data(web_data)
                        #     if result.status_code != 201:
                        #         self.post_error(result.text.web_data["url"].split("/job/")[1])
                        #         print("web data error" + web_data ["url"])
                        #         continue
                        #     else:
                        #         print(result)
                        #     data_count +=1
                        # else:
                        #     print("data error %s" % rent_item.find("a", href=True)["href"])
                    page_row += 1
                    data_b += 20
                except Exception as e:
                    self.browser.quit()
                    exit()
        
        

            
        
    def get_web_data(self,job_url:str):
        try:
            self.browser.get(job_url)
            data={}
            data["url"]=job_url
            if self.wait_element(By.CLASS_NAME, "col-sm-8"):
                print("page %s not found!" % (data["url"]))
                return None
            address=self.browser.find_elements(By.CLASS_NAME,"align-items-top")
            data["name"]=self.browser.find_element(By.CLASS_NAME,"title_4").text

            data["salary"]=self.get_salary((self.browser.find_element(By.CLASS_NAME,"job_salary").text))
            
            data["tenure"]=self.browser.find_element(By.CLASS_NAME,"data_trans").find_element(By.CLASS_NAME,"applicants").text.replace("\n",'')[4:]
            
            data["address"]=address[4].find_element(By.CLASS_NAME,"job_info_content").text
            
            data["URL"]=self.browser.find_element(By.NAME,"twitter:url").get_attribute('Content')
            
            data["district"]=self.get_dirstrict(data["address"].split(" ")[1])

            job_position = address[3].text.replace('\n','')[5:].split("、")
            for position in job_position:
                pk = self.job_position(position)
                if pk != None:
                    data["job_position"] = pk

            #work_hour
            data["work_hour"]=self.working_hour((address[0]).text.replace('\n'," "))
            
            #benfit
            benefitlist=self.browser.find_elements(By.XPATH,"//div[@class='content_items job_benefits']")
            for i in benefitlist:
                if i.find_element(By.XPATH, "//h6[@class='title_6 title spy_item']").text == "職缺福利":
                    print(benefitlist.find_element(By.CLASS_NAME, "body_2").text)
            
            return data
        except Exception as e:
            traceback.print_exc()
            print(data)
            with open("error_log", 'w') as file:
                file.write("{} {}\n{}".format(data["name"], data["url"], e))
            return data["url"]

            