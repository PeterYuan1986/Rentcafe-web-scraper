from datetime import datetime
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

# using random delay for time.sleep()
delays = [7, 4, 6, 2, 10, 19]
delay = np.random.choice(delays)
CHROMEDRIVER_PATH = r"C:\Program Files (x86)\Google\Chrome\chromedriver.exe"
myProxy = ['167.172.123.221', '129.21.253.179', '159.89.221.73']
proxys = np.random.choice(myProxy)
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': proxys,
    'ftpProxy': proxys,
    'sslProxy': proxys,
})


def get_review(url,save):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
    driver.get(url)

    time.sleep(delay)
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    review_num = 0
    final_data = []
    num_page = 1
    info_scraped = {}
    info_scraped['name'] = None
    info_scraped['link'] = None
    info_scraped['address'] = None
    info_scraped['city'] = None
    info_scraped['state'] = None
    info_scraped['ratings'] = None
    info_scraped['zipcode'] = None
    # retrieve the total page number, if there is no information about this, it means the reviews have less than one full page, set page number to 1.

    listings = soup.find_all('li', {'class': 'listing-details'})
    # print(listings)
    for i in range(len(listings)):
        try:
            name = listings[i].find('div', {'class': 'listing-name-address'}).find('a', href=True)
            name_text = name.text
            link = name['href']
            info_scraped['name'] = name_text
            info_scraped['link'] = link
            print(name_text)
            print(link)
        except:
            pass
        try:
            rating = listings[i].find('span', {'class': 'rating-stars'})['data-starrating']
            info_scraped['ratings'] = rating
        except:
            pass
        try:
            address = listings[i].find('span', {'itemprop': 'streetAddress'}).text
            info_scraped['address'] = address
        except:
            pass
        try:
            city = listings[i].find('span', {'itemprop': 'addressLocality'}).text
            info_scraped['city'] = city
        except:
            pass
        try:
            state = listings[i].find('span', {'itemprop': 'addressRegion'}).text
            info_scraped['state'] = state
        except:
            pass
        try:
            zipcode = listings[i].find('span', {'itemprop': 'postalCode'}).text
            info_scraped['zipcode'] = zipcode
        except:
            pass
        try:
            beds = listings[i].find_all('li', {'class': 'data-beds'})
            cost = listings[i].find_all('li', {'class': 'data-rent'})
            for b in range(len(beds)):
                type = beds[b].text
                value  = cost[b].text
                info_scraped[type] = value
        except:
            pass
        final_data.append(info_scraped.copy())

    driver.quit()

    df = pd.DataFrame(final_data)
    df.to_csv(save)

# for i in range(1,21):
#     url = f'https://www.rentcafe.com/apartments-for-rent/us/nc/?page=%s'%i
#     resreview = get_review(url,f"info_scraped_%s.csv"%i)
df = pd.read_csv("info_scraped_1.csv")
for i in range(2,21):
    df1 = pd.read_csv(f"info_scraped_%s.csv"%i)
    df = pd.concat([df, df1], axis=0)
df.to_csv("info_scraped_nc.csv")
