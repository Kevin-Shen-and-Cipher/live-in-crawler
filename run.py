from src.apartment.apartment_591_crawler import Apartment591Carwler
from src.apartment.apartment_happy_crawler import ApartmentHappy
from src.job.job_1111_crawler import job_1111_crawler
# Apartment591Carwler = Apartment591Carwler()
# Apartment591Carwler.crawler_591()
# ApartmentHappy = ApartmentHappy()
# data = ApartmentHappy.get_web_url()
job_1111_crawler = job_1111_crawler()
job_1111_crawler.job_link()
#print(job_1111_crawler.get_web_data("https://www.1111.com.tw/job/91416768/"))