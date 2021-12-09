from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time 

url = "https://www.linkedin.com/checkpoint/lg/sign-in-another-account"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=50)
    page = browser.new_page()
    page.goto(url)
    page.fill('input#username', 'oladayo@me.com')
    page.fill('input#password', 'ABab12!@')
    page.click('button[type=submit]')
    time.sleep(60)
    page.is_visible('div.scaffold-layout__sidebar')
    print(page.inner_html('body'))