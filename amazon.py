'''
Amazon product comment collector
'''
# Importing libraries
import requests
import urllib.request as urllib2
import re
import sys
from bs4 import BeautifulSoup


def kurti_read():
    """
    :return: returns bs4 soup
    """
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    product_kurti = 'https://www.amazon.in/kurti-Ethnic-Wear-Women/s?ie=UTF8&page=1&rh=n%3A1571271031%2Ck%3Akurti'
    kurti_page = requests.get(product_kurti, headers=headers)
    return kurti_page


def get_product_link_from_page(parent_link):
    """
    :param parent_link: string: a http link
    :return:list: a list of strings of web links
    """
    get_links = []
    kurti_soup = BeautifulSoup(parent_link.content, 'lxml')
    all_kurti_links = kurti_soup.find_all("a")
    for each_kurti_link in all_kurti_links:
        link = each_kurti_link.get("href")
        pattern = re.compile('https:\/\/www.amazon.in\/[A-Za-z0-9_\-]+\/dp\/[A-Z0-9]+')
        try:
            result = pattern.findall(link)
            if result:
                get_links.append(result[0])
        except TypeError:
            pass
    return list(set(get_links))

def get_product_title(product_link):
    """
    get each product title
    """
    
    product_title = []
    for each_product in product_link:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        product_link_open = requests.get(each_product, headers=headers)
        product_soup = BeautifulSoup(product_link_open.content, 'lxml')
        product_title = product_soup.find("div", {'id' : 'titleSection'})
        product_title.append(product_title.find("h1", {'id' : 'title'}).text.strip())
    return (product_title)


def get_product_rating(product_link):
    """
    get each product rating
    """
    
    product_rating = []
    for each_product in product_link:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        product_link_open = requests.get(each_product, headers=headers)
        product_soup = BeautifulSoup(product_link_open.content, 'lxml')
        product_review = product_soup.find("div", {'id' : 'averageCustomerReviews'})
        try:
            product_rating.append(product_review.find("span", {'class' : 'a-icon-alt'}).text.strip())
        except AttributeError:
            print('No rating yet.')
            pass
    return (product_rating)


def fetch_comments_link(product_link):
    """
    read comments from product link page.
    """
    
    product_comment = []
    get_links = []
    for each_product in product_link:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        product_link_open = requests.get(each_product, headers=headers)
        product_soup = BeautifulSoup(product_link_open.content, 'lxml')
        all_comments_link = product_soup.find_all("a")
        for each_reviews_link in all_comments_link:
            link = each_reviews_link.get("href")
            pattern = re.compile('https://www.amazon.in/.*/product-reviews/\w+/')
            try:
                result = pattern.findall(link)
                if result:
                    get_links.append(result)
            except TypeError:
                pass
    return list(set(get_links))



    
def get_next_parent_page_link(parent_link):
    """
    get the next page containing catalog of product..in real life this is the page 2,3,4 of the search result

    returns : string : is a web link
    """
    #todo




if __name__ == '__main__':
    parent_link = kurti_read()
    product_link = get_product_link_from_page(parent_link)
    print(fetch_comments_link(product_link))
