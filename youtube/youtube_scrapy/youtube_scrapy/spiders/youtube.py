import scrapy
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from youtube_scrapy.items  import YoutubeScrapyItem

class YoutubeSpider(scrapy.Spider):
    name = 'youtube'

    def start_requests(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        url = 'https://www.youtube.com/c/JohnWatsonRooney/videos'

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)

        videos = driver.find_elements(By.CSS_SELECTOR, 'ytd-grid-video-renderer')

        for video in videos:
            href = video.find_element(By.XPATH, './/*[@id="video-title"]').get_attribute('href')
            yield scrapy.Request(href)


    def parse(self, response):
        item = YoutubeScrapyItem()
        item['title'] = response.css('title ::text').get()
        item['views'] = response.xpath('//meta[@itemprop="interactionCount"]/@content').get()
        item['posted'] = response.xpath('//meta[@itemprop="uploadDate"]/@content').get()


        yield item 

