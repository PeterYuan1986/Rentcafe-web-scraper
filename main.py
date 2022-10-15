from bs4 import BeautifulSoup
import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
links_with_text = []
final_city_links = []
info_scraped = {}


# scraps all urls on the page
def parse_url(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    # t.sleep(3)

    for a in soup.find_all('a', href=True, class_='css-1m051bw'):
        if a.text:
            print(a.text)
            # print(a['href'])
            links_with_text.append(a['href'])


# save only business URL
def clean_urls(links_with_text):
    for link in links_with_text:
        if (link[0:5] == "/biz/"):
            info_scraped['URL'] = "https://www.yelp.com" + link
            final_city_links.append(info_scraped['URL'])
    print(final_city_links)
    df = pd.DataFrame({'URL': final_city_links})
    return (df)


# main function takes in list of page numbers as input and scraps it
if __name__ == "__main__":
    for m in range(0, 231, 10):
        yelp_url = "https://www.yelp.com/search?cflt=restaurants&find_loc=charlotte&start=%s" % (m)
        print(m)
        scraped_data = parse_url(yelp_url)
    final_links = clean_urls(links_with_text)
    final_links.to_csv("url_yelp.csv")
