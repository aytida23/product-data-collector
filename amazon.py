'''
Amazon product total number of comments collector
'''
# Importing libraries
import requests
import urllib.request as urllib2
import re
import random
from bs4 import BeautifulSoup


def kurti_read(url):
    """
    :return: returns parsed html page
    """
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    #product_kurti = 'https://www.amazon.in/kurti-Clothing-Accessories/s?ie=UTF8&page=1&rh=n%3A1571271031%2Ck%3Akurti'
    kurti_page = requests.get(url, headers=headers)
    return (kurti_page)


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
    count = 0
    for each_product in product_link:
        head1 = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head2 = {'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head3 = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head4 = {'User-Agent': 'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head5 = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

        headrs = random.choice([head1,head2,head3,head4,head5])
        product_link_open = requests.get(each_product, headers=headrs)
        product_soup = BeautifulSoup(product_link_open.content, 'lxml')
        productName = product_soup.find("div", {'id' : 'titleBlock'})
        product_title.append(productName.find("span", {'id' : 'productTitle'}).text.strip())
        count += 1

    print(count)
    return (product_title)


def get_product_rating(product_link):
    """
    get each product rating
    """
    
    product_rating = []
    count = 0
    for each_product in product_link:
        head1 = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head2 = {'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head3 = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head4 = {'User-Agent': 'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head5 = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

        headrs = random.choice([head1,head2,head3,head4,head5])
        product_link_open = requests.get(each_product, headers=headrs)
        product_soup = BeautifulSoup(product_link_open.content, 'lxml')
        each_product_rating = product_soup.find("div", {'id' : 'averageCustomerReviews'})
        try:
            print(each_product_rating.find("span", {'class' : 'a-icon-alt'}).text.strip())
            count += 1
        except AttributeError:
            print('No rating yet.')
            pass
    print(count)
    return (product_rating)


def get_product_review(product_link):
    """
    get product total number of review
    """

    product_review = []
    count = 0
    for each_product in product_link:
        head1 = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head2 = {'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head3 = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head4 = {'User-Agent': 'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head5 = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

        headrs = random.choice([head1,head2,head3,head4,head5])
        product_link_open = requests.get(each_product, headers=headrs)
        product_soup = BeautifulSoup(product_link_open.content, 'lxml')
        each_product_review = product_soup.find("div", {'id' : 'averageCustomerReviews'})
        product_review.append(each_product_review.find("span", {'class' : 'a-size-base'}).text.strip())
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
        head1 = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head2 = {'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head3 = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head4 = {'User-Agent': 'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        head5 = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

        headrs = random.choice([head1,head2,head3,head4,head5])
        product_link_open = requests.get(each_product, headers=headrs)
        product_soup = BeautifulSoup(product_link_open.content, 'lxml')
        each_product_price = product_soup.find("div", {'id' : 'desktop_unifiedPrice'})
        prices = each_product_prices.find("span", {'class' : 'a-size-medium a-color-price'})
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


def get_next_parent_page_link():
    """
    get the next page containing catalog of product..in real life this is the page 2,3,4 of the search result

    returns : string : is a web link
    """
    #todo
    kurti_soup = BeautifulSoup(parent_link.content, 'lxml')
    bottom_next_page_bar = kurti_soup.find("div", {'id' : 'centerBelowMinus'})
    last_page = int(bottom_next_page_bar.find("span", {'class' : 'pagnDisabled'}).text.strip())
    for i in range(1, last_page+1):
        link = 'https://www.amazon.in/kurti-Clothing-Accessories/s?ie=UTF8&page={}&rh=n%3A1571271031%2Ck%3Akurti'.format(i)
        product_url = kurti_read(link)
    return (product_url)
        
    


if __name__ == '__main__':
    prod_urls = get_next_parent_page_link()
    parent_link = kurti_read(prod_urls)
    urls = get_product_link_from_page(parent_link)
    
    #get_product_title(product_link)
    #get_product_rating(product_link)
    #each_product_price = get_product_price(product_link)
