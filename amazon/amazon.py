from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import argparse

def grocery(parser):
    s = HTMLSession()

    deals_list = []
    searchterm = parser.item
    url = f"https://www.amazon.ca/s?k={searchterm}&i=grocery"

    def getdata(url):
        r = s.get(url)
        r.html.render(sleep=1)
        soup = BeautifulSoup(r.html.html, 'html.parser')

        return soup


    def getdeals(soup):
        products = soup.find_all("div",{"data-component-type": "s-search-result"})

        for item in products:
            title = item.find('span', {'class':'a-size-base-plus a-color-base a-text-normal'}).text.strip()
            short_title = item.find('span', {'class':'a-size-base-plus a-color-base a-text-normal'}).text.strip()[:25]
            link  = item.find('a', {'class':'a-link-normal a-text-normal'})['href']
            try:
                price = item.find('span', {'class': 'a-offscreen'}).text.replace('$','').strip()
            except:
                price = "absent"
            try:
                ratings = item.find('span', {'class': 'a-icon-alt'}).text.strip()
            except:
                ratings = "absent"
            try:
                reviews = item.find('span', {'class': "a-size-base"}).text.strip()
            except:
                reviews = 0
            

            saleitem = {
                'title': title,
                'short_title': short_title,
                'link': link,
                'price': price,
                'ratings': ratings,
                'reviews': reviews
            }
            deals_list.append(saleitem)

        return 

    def getnextpage(soup):
        pages = soup.find('ul', {'class': 'a-pagination'})
        if not pages.find('li', {'class': 'a-disabled a-last'}):
            url = 'https://www.amazon.ca' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
            return url
        else:
            return


    while True:
        soup = getdata(url)
        getdeals(soup)
        url = getnextpage(soup)
        if not url:
            break
        else:
            print(url)
            print(len(deals_list))

    df = pd.DataFrame(deals_list)
    df.to_csv('amazon.csv')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Amazon Grocery Scraper")
    parser.add_argument("-i","--item", type=str,
                    help="Amazon grocery item to search")
    args = parser.parse_args()

    grocery(args)
