'''
Amazon product total number of comments collector
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
    product_kurti = 'https://www.amazon.in/kurti-Clothing-Accessories/s?ie=UTF8&page=1&rh=n%3A1571271031%2Ck%3Akurti'
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
    count = 0
    for each_product in product_link:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        product_link_open = requests.get(each_product, headers=headers)
        product_soup = BeautifulSoup(product_link_open.content, 'lxml')
        product_review = product_soup.find("div", {'id' : 'averageCustomerReviews'})
        try:
            print(product_review.find("span", {'class' : 'a-icon-alt'}).text.strip())
            count += 1
        except AttributeError:
            print('No rating yet.')
            pass
    print(count)
    #return (product_rating)


def get_product_review(product_link):
    """
    get product total number of review
    """

    product_review = []
    count = 0
    for each_product in product_link:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        product_link_open = requests.get(each_product, headers=headers)
        product_soup = BeautifulSoup(product_link_open.content, 'lxml')
        product_reviews = product_soup.find("div", {'id' : 'averageCustomerReviews'})
        product_review.append(product_reviews.find("span", {'class' : 'a-size-base'}).text.strip())
        count += 1
        
    print(count)
    return(product_review)


def get_product_price(product_link):
    """
    get product total number of review
    """

    product_price = []
    count = 0
    for each_product in product_link:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        product_link_open = requests.get(each_product, headers=headers)
        product_soup = BeautifulSoup(product_link_open.content, 'lxml')
        product_prices = product_soup.find("div", {'id' : 'desktop_unifiedPrice'})
        prices = product_prices.find("span", {'class' : 'a-size-medium a-color-price'})
        product_price.append(prices.text.strip())
        count += 1
        
    print(count)
    return(product_price)
        


    

'''def fetch_product_review_link(product_link):
    """
    fetch reviews page lin from each product link page.
    """
    
    reviews_links = []
    for each_product in product_link:
        each_product_review_link = re.sub(r'/dp/','/product-reviews/', each_product)
        reviews_links.append(each_product_review_link)
        
    return list(set(reviews_links))'''


'''def fetch_max_page_limit(product_reviews_link):
    """
    fetch each individual comment from each product review page
    """

    max_page_number = []
    for link in product_reviews_link:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        review_link_open = requests.get(link, headers=headers)
        review_soup = BeautifulSoup(review_link_open.content, 'lxml')
        page_numbers = review_soup.find_all("li", {'data-reftag' : 'cm_cr_arp_d_paging_btm'})
        for each_page_num in page_numbers:
            max_page_number.append((each_page_num).text)
    return(max_page_number)'''


'''def get_next_parent_page_link(parent_link):
    """
    get the next page containing catalog of product..in real life this is the page 2,3,4 of the search result

    returns : string : is a web link
    """
    #todo'''




if __name__ == '__main__':
    parent_link = kurti_read()
    product_link = get_product_link_from_page(parent_link)
    each_product_title = get_product_title(product_link)
    get_product_rating(product_link)
    each_product_price = get_product_price(product_link)
