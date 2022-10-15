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


def get_review(url, res_name, res_address):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, proxy=proxy, options=options)
    driver.get(url)

    time.sleep(delay)
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    review_num = 0
    final_data = []
    num_page = 1
    info_scraped = {}
    info_scraped['reviewer_name'] = None
    # info_scraped['reviewer_stat'] = None
    info_scraped['reviewer_friends'] = None
    info_scraped['reviewer_reviews'] = None
    info_scraped['reviewer_photos'] = None
    info_scraped['ratings'] = None
    info_scraped['comment'] = None
    info_scraped['review_date'] = None
    info_scraped['reviewer_origin'] = None
    info_scraped['reviewer_profile'] = None
    # retrieve the total page number, if there is no information about this, it means the reviews have less than one full page, set page number to 1.
    try:
        # total_page = driver.find_element_by_xpath(
        #     '/html/body/div[2]/div[3]/yelp-react-root/div/div[3]/div/div/div[2]/div/div[1]/div[2]/section[2]/div[2]/div/div[4]/div[2]/span').text
        total_page = soup.find('div', {'class': 'pagination__09f24__VRjN4 border-color--default__09f24__NPAKY'}).find(
            'span', {'class': 'css-chan6m'}).text
        print(total_page)
        totalpage = [int(s) for s in total_page.split() if s.isdigit()]

        num_page = totalpage[-1]
        print(num_page)
        # num_page = 1

    except:
        print(None)

    # iterate through all pages

    print(url)
    for page_np in range(num_page)[2:]:
        print('[{}] {} scraped page out of {}'.format(datetime.now(), page_np, num_page))
        time.sleep(2)
        url_ = url + f'&start={page_np * 10}'
        driver.get(url_)
        # soup = BeautifulSoup(page, 'lxml')
        soup2 = BeautifulSoup(page, 'lxml')

        # retrieve all data on the site
        all = soup.find_all('div', {'class': "main-content-wrap main-content-wrap--full"})

        # special_all_stat = soup2.find_all('div',{'class': " margin-t0-5__373c0__1VMSL border-color--default__373c0__3-ifU"})
        special_all_reviews = soup2.find_all('li',
                                             {'class': 'margin-b5__09f24__pTvws border-color--default__09f24__NPAKY'})

        for i in range(len(special_all_reviews)):
            info_scraped = {}
            default = 'https://www.yelp.com'
            stat = ''
            origin = ''
            # retrieve reviewer name
            try:
                review = special_all_reviews[i].find('div', {
                    'class': 'review__09f24__oHr9V border-color--default__09f24__NPAKY'})
            except:
                continue

            review_num += 1
            try:
                special_user = review.find('a', {'class': "css-1m051bw", 'href': re.compile(r'/user')})

                info_scraped['reviewer_name'] = special_user.text
                # print(info_scraped['reviewer_name'])
            except:
                print(None)

            # retrieve reviewer statistic, like number of friends, number of reviews, elite or not.
            try:

                for j in special_all_reviews[i].find_all('span', {'class': 'css-1fnccdf'}):
                    stat += j.text
                    stat += " "
                # print(stat)
                info_scraped['reviewer_friends'] = stat.split()[0]
                info_scraped['reviewer_reviews'] = stat.split()[1]
                info_scraped['reviewer_photos'] = stat.split()[2]
            except:

                print(None)

            # retrieve the rating of this review
            try:

                info_scraped['ratings'] = \
                    special_all_reviews[i].find('div', {"aria-label": re.compile('star rating')})["aria-label"].split()[
                        0]
                # print(info_scraped['ratings'])
            except:
                print(None)

            # retrieve the comment text the reviewer left
            try:

                info_scraped['comment'] = special_all_reviews[i].find('p', {
                    'class': 'comment__09f24__gu0rG css-qgunke'}).find('span', {'class': 'raw__09f24__T4Ezm'}).text

                # print(info_scraped['comment'])
            except:

                print(None)

            # retrieve the date of review
            try:
                info_scraped['review_date'] = datetime.strptime(special_all_reviews[i].find('span', {
                    'class': 'css-chan6m'}).text, '%m/%d/%Y').date()

                # print(info_scraped['review_date'])
            except:
                print(None)
            print("********************************************************************************")

            final_data.append(info_scraped)

    address = res_address.strip()
    restaurant_name = [res_name] * review_num
    address = [address] * review_num

    driver.quit()

    df = pd.DataFrame(final_data)

    df['restaurant name'] = pd.Series(restaurant_name)
    df['address'] = pd.Series(address)
    df.index += 1
    print(df)
    return df


df = pd.read_csv('Res_info.csv')
urls = df['restaurant_url']
res_add = df['restaurant_address']
res_name = df['restaurant_name']
iteration_from = 0
iteration_end = len(urls)
review_data = []

for i in range(iteration_from, iteration_end):
    print(str(i) + " restaurant out of " + str(len(urls)))
    item = urls[i]
    name = res_name[i]
    address = res_add[i]
    resreview = get_review(item, name, address)
    review_data.append(resreview)
    review_all = pd.concat(review_data)
    review_all.to_csv("Reviews" + str(i) + "-" + str(name) + ".csv")
