import traceback

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from tqdm import tqdm

from .apartment_crawler import ApartmentCrawler


class ApartmentHappy(ApartmentCrawler):
    cities = [0, 2]
    total_number = 0

    def __init__(self) -> None:
        super().__init__()
        self.progress_bar = tqdm(total=self.data_limit, desc=f"Crawling apartments")
        self.init()

    def init(self):
        self.total_number = 0
        self.progress_bar.reset()

    def run(self):
        self.init()

        max_data = self.data_limit / len(self.cities)

        try:
            for city_id in self.cities:
                self.get_apartments(city_id=city_id, max_data=max_data)
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.browser.quit()

    def get_apartments(self, city_id: int, max_data: int):
        page = 0
        current_number = 0
        while current_number < max_data:
            url = f"https://rakuya.com.tw/rent/rent_search?search=city&city={city_id}&upd=1&page={page}"
            self.browser.get(url)

            page_source = self.browser.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            selector = "div.obj-item.clearfix a.obj-cover[href]"
            items = soup.select(selector)

            for item in items:
                url = item.get("href")
                data = self.get_apartment_data(url)

                if data is None:
                    continue

                self.post_data(data)

                current_number += 1
                self.total_number += 1

                self.progress_bar.update(1)

                if current_number == max_data:
                    break

            page += 1

    def get_name(self) -> str:
        selector = (
            "body > div.container > div.topbar > div.block__title > h2 > span.title"
        )

        name = self.browser.find_element(By.CSS_SELECTOR, selector).text

        return name

    def get_price(self) -> str:
        selector = "body > div.container > div.main-body > div.sidebar > div.block__info-main > div > span"

        price = self.browser.find_element(By.CSS_SELECTOR, selector).text
        price = price.replace("元", "").replace(",", "")
        price = int(price)

        return price

    def get_address(self) -> str:
        selector = "body > div.container > div.topbar > div.block__title > h1"

        content = self.browser.find_element(By.CSS_SELECTOR, selector).text

        address = content.split("/", 1)[0].strip()

        return address

    def get_district(self) -> int:
        address = self.get_address()

        district = self.find_district(address)

        return district

    def get_coordinate(self) -> str:
        selector = "#app_nearByLifeMap > section > div.itemInfoSection__header.flex.items-center.justify-between.gap-md > div > div > div > a"

        link_element = self.browser.find_element(By.CSS_SELECTOR, selector)

        link = link_element.get_attribute("href")

        try:
            coordinate = link.split("query=", 1)[1]
        except IndexError:
            coordinate = None

        return coordinate

    def get_rent_type(self) -> int:
        selector = "//li[./span[@class='list__label' and text()='類型']]/span[@class='list__content']"

        content = self.browser.find_element(By.XPATH, selector).text

        rent_type = self.find_rent_type(content)

        return rent_type

    def get_aparment_type(self) -> int:
        selector = "//li[./span[@class='list__label' and text()='類型']]/span[@class='list__content']"

        content = self.browser.find_element(By.XPATH, selector).text

        aparment_type = self.find_aparment_type(content)

        return aparment_type

    def get_room_type(self) -> int | None:
        selector = "//li[./span[@class='list__label' and text()='格局']]/span[@class='list__content']"

        try:
            content = self.browser.find_element(By.XPATH, selector).text
            room_type = self.find_room_type(content)
            return room_type
        except NoSuchElementException:
            return None

    def get_restrict(self):
        selector = "//li[./span[@class='list__label' and text()='性別要求']]/span[@class='list__content']"

        content = self.browser.find_element(By.XPATH, selector).text

        try:
            restrict = [self.find_restrict(content)]
            restrict = list(set(restrict))
        except Exception:
            restrict = [1]

        return restrict

    def get_device(self):
        selector = "//li[./span[@class='list__label' and text()='設備']]/span[@class='list__content']/b"

        elements = self.browser.find_elements(By.XPATH, selector)

        devices = [self.find_device(element.text) for element in elements]
        devices = list(set(devices))

        return devices

    def get_surrounding_facility(self):
        return []

    def get_apartment_data(self, url: str):
        self.browser.get(url)

        try:
            data = {
                "url": url,
                "name": self.get_name(),
                "price": self.get_price(),
                "address": self.get_address(),
                "district": self.get_district(),
                "coordinate": self.get_coordinate(),
                "rent_type": self.get_rent_type(),
                "apartment_type": self.get_aparment_type(),
                "room_type": self.get_room_type(),
                "restrict": self.get_restrict(),
                "device": self.get_device(),
                "surrounding_facility": self.get_surrounding_facility(),
            }
        except Exception as e:
            return None

        if self.check_data(data):
            return None

        return data
