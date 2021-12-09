from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

def close_modal(driver):
    try:
        modal_close = driver.find_element(By.CLASS_NAME, "modal__close")
        
        if modal_close:
            modal_close.click()
    except:
        pass

options = webdriver.ChromeOptions()

url = 'https://www.youtube.com/c/JohnWatsonRooney/videos'

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
close_modal(driver)


driver.get(url)
elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="video-title"]')))

driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
old_height = driver.execute_script("return document.documentElement.scrollHeight")
print(driver.execute_script("return document.documentElement.scrollHeight"))

driver.execute_script(f"window.scrollTo({old_height}, document.documentElement.scrollHeight);")
new_height = driver.execute_script("return document.documentElement.scrollHeight")
print(driver.execute_script("return document.documentElement.scrollHeight"))

while driver.find_element_by_tag_name('div'):
    
    driver.execute_script(f"window.scrollTo({old_height}, document.documentElement.scrollHeight);")
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    print(driver.execute_script("return document.documentElement.scrollHeight"))
    
    
    Divs=driver.find_element_by_tag_name('div').text
    
    if new_height == old_height:
        print('end')
        break
    else:
        old_height = new_height
        time.sleep(3)
        continue
print("Complete")

videos = driver.find_elements(By.CSS_SELECTOR, 'ytd-grid-video-renderer')

print(len(videos))

video_list =[]
for video in videos:
    title = video.find_element(By.XPATH, './/*[@id="video-title"]').text
    views = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[1]').text
    posted = video.find_element(By.XPATH,'.//*[@id="metadata-line"]/span[2]').text
    items = {
        'title' : title,
        'views' : views,
        'posted': posted
    }
    video_list.append(items)

df = pd.DataFrame(video_list)
print(df)

