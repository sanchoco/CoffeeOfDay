import time
import re
import setting_info
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


db = setting_info.db_connect()

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.starbucks.co.kr/menu/drink_list.do')
time.sleep(7)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')
drinks = soup.findAll("li", {"class": re.compile("menuDataSet")})
id = 0
for drink in drinks:
    image_tag = drink.find("img")
    image_url = image_tag['src']
    name = image_tag['alt']
    id = id + 1
    doc = {
        "product_id":id,
        "name": name,
        "img_url": image_url,
        "like": 0,
        "dislike": 0,
        "total_like":0,
    }
    db.daycoffee.insert_one(doc)
    print("completed", name)
