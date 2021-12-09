from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import os
import hashlib
from bs4 import BeautifulSoup
import time


def download_img(href):
    print(href)
    options = webdriver.ChromeOptions()
    options.headless = True
    url = href
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    time.sleep(3)
    page = BeautifulSoup(driver.page_source, "html.parser")


    images = page.findAll("img", {"class": "processed-image"})
    print(len(images))
    # image_list = []
    # i = 0
    for image in images:
        img = image["src"]
        print(img)
        if img.startswith('https:'):
            response = requests.get(img)

            if response.status_code == 200:
                filename = hashlib.sha256(bytes(url, "utf-8")).hexdigest()[:15] + ".jpeg"
                file_path = os.path.join("images", filename)

                with open(file_path, "wb") as fl:
                    fl.write(response.content)


options = webdriver.ChromeOptions()
options.headless = True

url = 'https://www.levi.com/CA/en_CA/clothing/men/shorts/c/levi_clothing_men_shorts'

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.get(url)
page = BeautifulSoup(driver.page_source, "html.parser")

image_grid = page.find("div", {"class": "results-grid -show"})

images = image_grid.findAll("div", {"class": "product-cell"})

for image in images:
    x = image.find("a", {"class": "product-link"}).get("href")
    download_img(''.join(['https://levi.com', x]))





