from src.job.job_crawler import job_crawler
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import traceback
import re
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
            data_count = 1
            page_row = 1
            data_b = 1
            error_flag = 0
            while data_count <= self.data_limit:
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
                        if data_count > self.data_limit:
                            exit()
                        web_data = self.get_web_data(job_item.find_all("a", href=True)[0]["href"])
                        if web_data != None and self.check_data(web_data) == False:
                            try:
                                result=self.post_data(web_data)
                                if result.status_code != 201:
                                    self.post_error(result.text,web_data["url"].split("/job/")[1].replace("/", ''))
                                    print("request failed! " + web_data ["url"])
                                    continue
                                else:
                                    print(result)
                                    error_flag = 0
                                data_count +=1
                            except:
                                print("post error")
                    page_row += 1
                    data_b += 20
                except Exception as e:
                    if error_flag >=3:
                        self.browser.quit()
                        exit()
                    error_flag += 1
                    traceback.print_exc()
                    continue
        self.browser.quit()
        
        

            
        
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

            data["salary"]=self.get_salary((self.browser.find_element(By.XPATH,"//div[@class='ui_items job_salary']//p[@class='body_2']").text))

            tenure_data = self.browser.find_element(By.XPATH, "//div[@class='content_items job_skill']//div[@class = 'body_2 description_info']//span[@class='job_info_content']").text
            try:
                if tenure_data == "不拘":
                    data["tenure"] = 0
                else:
                    data["tenure"] = int(tenure_data.replace("年以上工作經驗", ""))
            except:
                print("tenure error {}".format(tenure_data))
            data["address"]=address[4].find_element(By.CLASS_NAME,"job_info_content").text
            
            data["district"]=self.get_dirstrict(data["address"].split(" ")[1])

            job_position = address[3].text.replace('\n','')[5:].split("、")
            for position in job_position:
                pk = self.job_position(position)
                if pk != None:
                    data["job_position"] = pk

            #work_hour
            data["working_hour"]=self.working_hour((address[0]).text.replace('\n'," "))
            
            data["benefit"] = []
            #benfit don't know why but this way is only way it can get the benefit
            benefitlist=self.browser.find_elements(By.XPATH,"//div[@class='content_items job_benefits']")
            if len(benefitlist) == 1 or len(benefitlist) == 2:
                try:
                    benetfit_data = benefitlist[len(benefitlist)-1]
                    try:
                        benefit_content = benetfit_data.find_element(By.CLASS_NAME, "body_2").text.split("更多說明：")[0].split("福利制度：")[1].replace(" ", "")
                    except:
                        return None
                    temp = re.sub("\S{3}：", "text" ,benefit_content)
                    temp = temp.replace("\n", " ").replace(" text ", "、").split("、")
                    for k in temp:
                        if k != "":
                            data["benefit"].append({"name":k})
                except:
                    traceback.print_exc()
                    return None
            else:
                data["benefit"] == None
            try:
                company_link = self.browser.find_element(By.XPATH, "//a[@class='ui_card_company_link']").get_attribute('href')
                self.browser.get(company_link)
                map_url = self.browser.find_element(By.XPATH, "/html/body/main/div[6]/div[1]/div[2]/div[1]/div/div[1]/ul/li[2]/a").get_attribute('href')
            except:
                return None
            data["coordinate"] = map_url.split("?q=")[1]
            return data
        except Exception as e:
            traceback.print_exc()
            with open("error_log", 'w') as file:
                file.write("{} {}\n{}".format(data["name"], data["url"], e))
            return data["url"]

            