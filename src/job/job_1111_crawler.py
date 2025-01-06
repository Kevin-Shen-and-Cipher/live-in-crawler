from src.job.job_crawler import job_crawler
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import traceback
import re
import time
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


class job_1111_crawler(job_crawler):
    def __init__(self):
        self.region = [200]
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
            flag = 1; 
            # while data_count <= self.data_limit:
            while data_count <= self.data_limit:
                print(data_count)
                flag = 0 
                try:
                    # region_url=("https://www.1111.com.tw/search/job?c0=100{}&d0=140802%2C140803%2C140202&page={}").format(str(i), str(page_row))
                    
                    # 查詢雙北地區、軟體工程師等
                    region_url=("https://www.1111.com.tw/search/job?d0=140202%2C140802%2C140803&c0=100100%2C100200&page={}").format(str(page_row))
                    self.get_web(region_url)
                    if self.wait_element(By.CLASS_NAME,"search-content"):
                        print("Can not connect to the page %s, please check the internet status or 591 connection block" % (region_url))
                        exit(0)
                    page_element = BeautifulSoup(self.browser.page_source, "html.parser")
                    rent_list = page_element.find("div", {"class": "search-content"})
                    rent_list = rent_list.find_all("div", {"class": "job-card__content"})                 
                    for job_item in rent_list:
                        if data_count > self.data_limit:
                            exit()
                        web_data = self.get_web_data("https://www.1111.com.tw" + job_item.find_all("a", href=True)[0]["href"])
                        # if web_data != None and self.check_data(web_data) == False:
                        if web_data != None: # test benefit 的資料取消掉，無視它
                            try:
                                result=self.post_data(web_data)
                                print( "api response ", result.status_code )
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
            if self.wait_element(By.XPATH, "//*[@id=\"WORK_CONTENT\"]/div/div[7]/div/div/div/iframe"):
                print("page %s not found!" % (data["url"]))
                return None
            # address=self.browser.find_elements(By.CLASS_NAME,"mb-4")
            data["name"]=self.browser.find_element(By.XPATH,'//*[@id="COMPANY_INFO"]/div[1]/div[1]/div/a/p').text
            
            data["salary"]=self.get_salary((self.browser.find_element(By.XPATH,'//*[@id="WORK_CONTENT"]/div/div[2]/div/div/div').text))
            if data["salary"] == None:
                return None
            tenure_data = self.browser.find_element(By.XPATH, '//*[@id="REQUIREMENTS"]/div/div[3]/p[2]').text
            try:
                if tenure_data == "不拘":
                    data["tenure"] = 0
                else:
                    data["tenure"] = int(tenure_data.replace("年以上工作經驗", ""))
            except:
                print("tenure error {}".format(tenure_data))
            
            # 有時候商家會把供
            try: 
                data["address"]=self.browser.find_element(By.XPATH,'//*[@id="WORK_CONTENT"]/div/div[7]/div/div/p').text
            except: 
                data["address"]=self.browser.find_element(By.XPATH,'//*[@id="WORK_CONTENT"]/div/div[6]/div/div/p').text
            try: 
                district = self.browser.find_element(By.XPATH,'//*[@id="__nuxt"]/div/main/div/div[1]/div/div/div[2]/div[1]/div[3]/div').text
                data["district"]=self.get_dirstrict(data["address"][3:6])
            except: 
                return None
            if(data["district"] == None):
                return None 

            job_position = self.browser.find_element(By.XPATH,'//*[@id="__nuxt"]/div/main/div/div[1]/div/div/div[2]/h1').text
            # print(job_position)
            pk = self.job_position(job_position)
            if pk != None:
                data["job_position"] = pk
            else: 
                return None

            #work_hour
            data["working_hour"]= self.working_hour(self.browser.find_element(By.XPATH,'//*[@id="WORK_CONTENT"]/div/div[5]/div/ul/li/p').text)
            data["benefit"] = []
            # print("working_hour ", data)
            # benefit 不做
            #benfit don't know why but this way is only way it can get the benefit
            # benefitlist=self.browser.find_elements(By.XPATH,"//div[@class='content_items job_benefits']")
            # if len(benefitlist) == 1 or len(benefitlist) == 2:
            #     try:
            #         benetfit_data = benefitlist[len(benefitlist)-1]
            #         try:
            #             benefit_content = benetfit_data.find_element(By.CLASS_NAME, "body_2").text.split("更多說明：")[0].split("福利制度：")[1].replace(" ", "")
            #         except:
            #             return None
            #         temp = re.sub("\S{3}：", "text" ,benefit_content)
            #         temp = temp.replace("\n", " ").replace(" text ", "、").split("、")
            #         for k in temp:
            #             if k != "":
            #                 data["benefit"].append({"name":k})
            #     except:
            #         traceback.print_exc()
            #         return None
            # else:
            #     data["benefit"] == None

            ## 因為他有時候在 6, 有時候在 7
            try: 
                iframe = self.browser.find_element(By.XPATH, "//*[@id=\"WORK_CONTENT\"]/div/div[7]/div/div/div/iframe")  
                map_url = iframe.get_attribute('src')[-22:]
                print("found ", map_url)
            except: 
                try: 
                    self.browser.switch_to.default_content()
                    iframe = self.browser.find_element(By.XPATH, "//*[@id=\"WORK_CONTENT\"]/div/div[6]/div/div/div/iframe")  
                    map_url = iframe.get_attribute('src')[-22]
                    print("found ", map_url)
                except:
                    print("not found google map on ", data["url"])
                    return None
            self.browser.switch_to.default_content()
            
            data["coordinate"] = map_url
            print(data)

            return data
        except Exception as e:
            traceback.print_exc()
            with open("error_log", 'w') as file:
                file.write("{} {}\n{}".format(data["name"], data["url"], e))
            return data["url"]

            