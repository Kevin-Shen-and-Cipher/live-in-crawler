from src.apartment.apartment_591_crawler import Apartment591Carwler
from src.apartment.apartment_happy_crawler import ApartmentHappy
# Apartment591Carwler = Apartment591Carwler()
# data = Apartment591Carwler.get_web_data("https://rent.591.com.tw/home/13636350")
# result = Apartment591Carwler.post_data(data)
ApartmentHappy = ApartmentHappy()
data = ApartmentHappy.get_web_url()
print(data)
