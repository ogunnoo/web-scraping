from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup
import time
##Using playwright codegen website

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to https://www.linkedin.com/
    page.goto("https://www.linkedin.com/")
    # Click [placeholder=" "]
    page.click("[placeholder=\" \"]")
    # Fill [placeholder=" "]
    page.fill("[placeholder=\" \"]", "oladayo@me.com")
    # Click text=Password Show >> [placeholder=" "]
    page.click("text=Password Show >> [placeholder=\" \"]")
    # Fill text=Password Show >> [placeholder=" "]
    page.fill("text=Password Show >> [placeholder=\" \"]", "ABab12!@")
    # Click [data-test-id="hero__content"] >> text=Sign in
    # with page.expect_navigation(url="https://www.linkedin.com/feed/?trk=homepage-basic_signin-form_submit"):
    with page.expect_navigation():
        page.click("[data-test-id=\"hero__content\"] >> text=Sign in")
    # assert page.url == "https://www.linkedin.com/feed/?trk=homepage-basic_signin-form_submit"
    # Click text=Oladayo Ogunnoiki
    # with page.expect_navigation(url="https://www.linkedin.com/in/oladayo-ogunnoiki-73264580/"):
    with page.expect_navigation():
        page.click("text=Oladayo Ogunnoiki")
    # ---------------------
    time.sleep(10)

    profile_page = BeautifulSoup(page.inner_html('body'), "html.parser")
    name = profile_page.find("h1", {"class": "text-heading-xlarge inline t-24 v-align-middle break-words"}).text
    title = profile_page.find("div", {"class": "text-body-medium break-words"}).text
    connections = profile_page.find("span", {"class": "link-without-visited-state"}).text

    print(name)
    print(title)
    print(connections)


    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)
