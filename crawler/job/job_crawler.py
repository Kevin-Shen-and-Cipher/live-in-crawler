from abc import ABC, abstractmethod
from webbrowser import Chrome
from crawler.crawler import Crawler
from job.job_sql import JobSql


class JobCrawler(ABC, Crawler):

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
