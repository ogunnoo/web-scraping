from helium import *
from bs4 import BeautifulSoup
import pandas as pd 
import argparse

def scrape(args):
    url = "https://www.linkedin.com/checkpoint/lg/sign-in-another-account"

    s =  start_firefox(url=url)

    write(args.username, into='Email or Phone')
    write(args.password, into='Password')
    click('Sign in')
    wait_until(Text('Oladayo Ogunnoiki').exists)
    click('Oladayo Ogunnoiki')
    wait_until(Text('Oladayo Ogunnoiki').exists)
    profile_page = BeautifulSoup(s.page_source, "html.parser")

    name = profile_page.find("h1", {"class": "text-heading-xlarge inline t-24 v-align-middle break-words"}).text
    title = profile_page.find("div", {"class": "text-body-medium break-words"}).text
    connections = profile_page.find("span", {"class": "link-without-visited-state"}).text

    info = {"name": [name.strip()],
                "title": [title.strip()],
                "connections": [connections.strip()]}

    print(info)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="LinkedIN Scraper")
    parser.add_argument("-u","--username", type=str,
                    help="LinkedIn User Name")
    parser.add_argument("-p","--password", type=str,
                    help="LinkedIn Password ") # Type password within ' ' single quotes
    args = parser.parse_args()

    scrape(args)
