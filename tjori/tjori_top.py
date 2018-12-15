'''
Tjori's product info collector
'''

# Importing libraries
import requests
import re
import random
from bs4 import BeautifulSoup
import pandas as pd
import logging
from fake_useragent import UserAgent
import time
from multiprocessing import Pool
import os



def get_page_soup(link):
    """
    get the bs4 soup of a page
    :param link:string: http link
    :return: bs4 soup
    """
    
    try:
            
        product_link_open = requests.get(link, headers=headerrs(), proxies=proxies())
        print(product_link_open.status_code)
    except requests.exceptions.ConnectionError:
        product_link_open.status_code = "Connection refused"
    
    return BeautifulSoup(product_link_open.content, 'lxml')


def read_proxy_file():
    proxy_list = []
    with open("proxies.txt") as f:
        raw_data = f.read()
        proxies_list = raw_data.split("\n")
        for proxy in proxies_list:
            if check_proxy_validity(proxy):
                proxy_list.append({'http': proxy})
    return proxy_list


def check_proxy_validity(ip):
    """
    checks validity of a proxy address
    :param ip: string
    :return: bool
    """
    try:
        status = requests.get("https://www.google.com", headers=headerrs(), proxies={'http': ip}, timeout=0.5)
        if str(status.status_code) == '200':
            return True
        return False
    except Exception:
        return False


def proxies():
    """
    :return: string
    """
    try:
        return random.choice(PROXY_LIST)
    except NameError:
        assert "SET PROXY_LIST=read_proxy_file()"



def headerrs():
    """
    return different random headers
    """
    ua = UserAgent()

    head1 = {'User-Agent': ua.random,
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
             'Accept-Encoding': 'none',
             'Accept-Language': 'en-US,en;q=0.8',
             'Connection': 'keep-alive'
             }

    return head1



def get_product_link_from_page(search_page_link):
    """
    :param search_page_link: string: a http link
    :return:list: a list of strings of web links
    """

    get_links = []
    main_page = requests.get(search_page_link, headers=headerrs())
    time.sleep(10)
    main_page_soup = BeautifulSoup(main_page.content, 'lxml')
    all_prod_links = main_page_soup.find_all('a')
    for each_prod_link in all_prod_links:
        link = each_prod_link.get('onclick')
        pattern = re.compile('\/+p+\/[a-z_-]+\/+[0-9]+\/')
        result = pattern.findall(str(link))
        if result:
            result = ''.join(result)
            updated_result = 'https://www.tjori.com'+result
            get_links.append(updated_result)
    return list(set(get_links))


def get_product_title(product_page_soup):
    """
    get each product title
    :param product_page_soup: bs4 soup: soup of a product page
    :return: string: product name
    """
    
    productname = product_page_soup.find('div', {'itemtype' : 'http://schema.org/Product'})
    product_title = productname.find('h1').text.strip()
    return product_title

def get_product_price(product_page_soup):
    """
    get product price
    :param product_page_soup: bs4 soup: soup of a product page
    :return: string
    """

    productprice = product_page_soup.find('span', {'itemtype' : 'http://schema.org/Offer'}).text.strip()
    return productprice


def get_next_parent_page_link(parent_link):
    """
    get the next page containing catalog of product..in real life this is the page 2,3,4 of the search result
    @:param parent_link: string: http link
    :returns : list: string : is a web link
    """
    page_linkss = []
    link = 'https://www.tjori.com/apparel/tops-crop-tops-shirts-shirt-dresses/'
    page_linkss.append(link)
    return page_linkss

def read_product_page_data(link):
    """
    get all values from a product page data
    :param link:string: http link
    :return:string
    """

    soup = get_page_soup(link)
    product_title = get_product_title(soup)
    product_price = get_product_price(soup)
    print(['Product title : '+str(product_title)+', Product Price : '+str(product_price)])
    return(['Product link : '+str(link)+', Product title : '+str(product_title)+', Product Price : '+str(product_price)])
  
    
def full_data_search_page(search_page_link):
    """

    :param search_page_link:
    :return:
    """
    all_product_links = get_product_link_from_page(search_page_link)
    create_file_ifnotexist(search_page_link.replace("/",""))
    with open(search_page_link.replace("/", ""), "a") as f:
        for link in all_product_links:
            individual_product = read_product_page_data(link)
            if individual_product:
                f.write(",\t".join(map(str,individual_product))+"\n")


def create_file_ifnotexist(filename):
    """

    :param filename:
    :return:
    """
    if not os.path.exists(filename):
        f = open(filename, "w")
        f.close()


def get_all_product_data(parent_link):
    """
    mother load
    :param parent_link:string: http
    :return:list of list
    """
    all_search_page_links = list(set(get_next_parent_page_link(parent_link)))
    #for link in all_search_page_links:
        #create_file_ifnotexist(link)
    with Pool(10) as p:
        p.map(full_data_search_page, all_search_page_links)


if __name__ == '__main__':
    LEFT_OVER_LINK = []
    PROXY_LIST = read_proxy_file()
    link = 'https://www.tjori.com/apparel/tops-crop-tops-shirts-shirt-dresses/'
    get_all_product_data(link)

    
