from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd 
import argparse


def scrape(args):
    global driver

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    url = "https://www.linkedin.com/checkpoint/lg/sign-in-another-account"

    driver.get(url)

    username = driver.find_element(By.ID, 'username')
    username.clear()
    username.send_keys(args.username)
    password = driver.find_element(By.ID, 'password')
    password.clear()
    password.send_keys(args.password)
    driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()

    page = BeautifulSoup(driver.page_source, "html.parser")
    button = page.find("div", {"class": "scaffold-layout__sidebar"})


    print(button.find("a").get('href'))

    profile = "".join(["https://www.linkedin.com", button.find("a").get('href')])
    driver.get(profile)

    profile_page = BeautifulSoup(driver.page_source, "html.parser")

    name = profile_page.find("h1", {"class": "text-heading-xlarge inline t-24 v-align-middle break-words"}).text
    title = profile_page.find("div", {"class": "text-body-medium break-words"}).text
    connections = profile_page.find("span", {"class": "link-without-visited-state"}).text
    about = profile_page.find("div", {"class": "inline-show-more-text inline-show-more-text--is-collapsed mt4 t-14"}).text

    info = {"name": [name.strip()],
            "title": [title.strip()],
            "connections": [connections.strip()],
            "about": [about.strip()]}

    pd.DataFrame.from_dict(info).to_csv("profile.csv")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="LinkedIN Scraper")
    parser.add_argument("-u","--username", type=str,
                    help="LinkedIn User Name")
    parser.add_argument("-p","--password", type=str,
                    help="LinkedIn Password")
    args = parser.parse_args()

    scrape(args)

