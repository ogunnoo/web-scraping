import scrapy
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from leviscrape.items  import LeviscrapeItem


class LeviSpider(scrapy.Spider):
    name = 'levi'
    
    def start_requests(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        url = 'https://www.levi.com/CA/en_CA/clothing/men/shorts/c/levi_clothing_men_shorts'

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        driver.get(url)

        images = driver.find_elements(By.CSS_SELECTOR, 'div.product-cell')
        for image in images:
            href = image.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[3]/div/div/div/div/div/div[2]/div[1]/a').get_attribute('href')
            yield scrapy.Request(href)


    def parse(self, response):
        raw_images = LeviscrapeItem()
        raw_images['image'] = "bread"

        yield raw_images
