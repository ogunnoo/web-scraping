import os
import time
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import IPython


def close_modal(driver):
    try:
        modal_close = driver.find_element_by_class_name("modal__close")

        if modal_close:
            modal_close.click()
    except:
        pass


def extract_image(image):
    link = image.get("src")

    if link == None or not link.startswith("http"):
        link = image.get("data-src")

    if not link.startswith("http"):
        link = None

    return link


def init_driver(fetcher):
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # options.add_argument("--disable-infobars")
    # options.add_argument("start-maximized")
    # options.add_argument("--disable-extensions")

    tab = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def fetcher_with_tab(*args, **kwargs):
        return fetcher(*args, **kwargs, driver=tab)

    return fetcher_with_tab


def product_page_scraper(url, driver=None):
    driver.get(url)
    time.sleep(2)
    page = BeautifulSoup(driver.page_source, "html.parser")
    close_modal(driver)

    choices = page.find("div", {"class": "swatches"})
    if choices == None:
        return []

    choices = choices.findAll("li")

    choices = list(map(lambda choice: choice.get("code"), choices))

    image_links = []

    for choice in choices:
        try:
            time.sleep(2)
            choice_button = driver.find_element_by_xpath(f'//li[@code="{choice}"]')
            choice_button.click()
            time.sleep(3)

            product_page = BeautifulSoup(driver.page_source, "html.parser")

            images = product_page.findAll("img", {"class": "processed-image"})

            if len(images) > 0:
                image_links.extend(
                    list(filter(lambda x: x != None, list(map(extract_image, images))))
                )
        except:
            continue

    return image_links


def product_list_scraper(url, driver=None):
    item_data = []
    page_idx = 0

    while page_idx != -1:
        print(page_idx)

        driver.get(url + f"?page={page_idx}")
        time.sleep(3)
        page = BeautifulSoup(driver.page_source, "html.parser")
        close_modal(driver)

        page_idx = (page_idx + 1) if page.find("li", {"class": "next-btn"}) else -1

        item_grid = page.find("div", {"class": "results-grid -show"})
        if item_grid == None:
            continue

        items = item_grid.findAll("div", {"class": "product-cell"})

        for item in items:

            single_item_data = {
                "name": item.find("div", {"class": "product-name"}).text.strip(),
                "url": "https://www.levi.com"
                + item.find("a", {"class": "product-link"}).get("href"),
            }

            image_urls = product_page_scraper(single_item_data["url"], driver)

            if len(image_urls) > 0:
                single_item_data["image_urls"] = image_urls
                item_data.append(single_item_data)

    return item_data


@init_driver
def crawler(root_url, save_dir, driver=None):
    driver.get(root_url)
    time.sleep(3)
    close_modal(driver)

    shop_button = driver.find_element_by_class_name("top-nav__item-btn")
    shop_button.click()

#    page = BeautifulSoup(driver.page_source, "html.parser")
#
#    navigation = page.find("nav", {"class": "l2-items"})
#
#    nav_buttons = navigation.findAll("button", {"class": "l2-items__link"})
#
#    nav_ids = list(
#        map(lambda nb: {"id": nb.get("id"), "name": nb.text.strip()}, nav_buttons)
#    )
#    time.sleep(3)
#
#    sections = []
#
#    for nav_id in nav_ids:
#        product_section = driver.find_element_by_id(nav_id["id"])
#        product_section.click()
#        time.sleep(3)
#
#        section_page = BeautifulSoup(driver.page_source, "html.parser")
#
#        section_page_links = section_page.findAll("a", {"class": "nav-l3__item--link"})
#
#        section_page_links = list(
#            filter(
#                lambda x: x != None,
#                list(
#                    map(
#                        lambda spl: {
#                            "section": nav_id["name"],
#                            "subsection": spl.text.strip(),
#                            "url": "https://www.levi.com" + spl.get("href"),
#                        }
#                        if spl.get("href")
#                        else None,
#                        section_page_links,
#                    )
#                ),
#            )
#        )
#
#        if len(section_page_links) > 0:
#            sections.extend(section_page_links)
#
#    for idx, section in enumerate(sections):
#        print(
#            f"Scraping [{idx+1}/{len(sections)}]: {section['section']} {section['subsection']}"
#        )
#        data = product_list_scraper(section["url"], driver)
#
#        if len(data) > 0:
#            section["data"] = data
#
#        with open(
#            os.path.join(
#                save_dir, f"{section['section']}_{section['subsection']}.json"
#            ),
#            "w",
#        ) as fl:
#            json.dump(section, fl)
#
#    driver.close()
    return sections


ROOT_DIR = "scraped_data"
sections = crawler("https://www.adidas.ca/en", ROOT_DIR)
#with open("complete_data.json", "w") as fl:
#    json.dump(sections, fl)

#IPython.embed()

while driver.find_element_by_tag_name('div'):
    
    driver.execute_script(f"window.scrollTo({old_height}, document.documentElement.scrollHeight);")
    new_height = driver.execute_script("return document.documentElement.scrollHeight") + 200
    print(new_height)
    print(old_height)
    print(driver.execute_script("return document.documentElement.scrollHeight"))
    
    
    Divs=driver.find_element_by_tag_name('div').text
    
    if new_height == old_height:
        print('end')
        break
    else:
        old_height = new_height
        #page = BeautifulSoup(driver.page_source, "html.parser")
        #images = page.findAll("a", {"id": "video-title"})
        time.sleep(1)
        
        continue
