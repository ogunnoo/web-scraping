from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



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

videos = driver.find_elements(By.CSS_SELECTOR, 'ytd-grid-video-renderer')
video_list =[]

for video in videos:
    href = video.find_element(By.XPATH, './/*[@id="video-title"]').get_attribute('href')
    video_list.append(href)
    print(href)
