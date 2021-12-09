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
options.headless = True
url = 'https://www.levi.com/CA/en_CA/premium/levis-pride-liberation-shortalls/p/A00530000'

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
close_modal(driver)

driver.get(url)

images = driver.find_elements(By.CSS_SELECTOR, 'img')
print(len(images))
image_list = []
for image in images:
     #href = image.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/img').get_attribute('src')
     #image_list.append(href)
     if image.get_attribute('src').startswith('https:'):
        print(image.get_attribute('src'))
