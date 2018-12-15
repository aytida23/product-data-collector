'''
Nicobar's product info collector
'''

# Importing libraries
import requests
import random
from bs4 import BeautifulSoup
import json
import re
import time
from fake_useragent import UserAgent
from multiprocessing import Pool
import os


def get_page_json(link):
    """
    get the json data of a page
    :param link:string: http link
    :return: json data in a dataframe
    """

    res = requests.get(link, headers=headerrs()).json()
    time.sleep(5)
    return res['data']


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
    prod_page_res = requests.get(search_page_link, headers=headerrs()).json()
    time.sleep(5)
    for each_prod_url in prod_page_res['results']['data']:
        prod_url = each_prod_url['url']
        pattern = re.compile('[0-9]+/')
        result = pattern.findall(prod_url)
        updated_prod_url = 'https://www.nicobar.com/myapi/pdp/'+''.join(result)
        get_links.append(updated_prod_url)
    
    return (list(set(get_links)))



def get_product_title(product_page_data):
    """
    get product title
    :param product_page_data: json data of a product page
    :return: string: product name
    """

    return product_page_data['title']



def get_product_price(product_page_data):
    """
    get product price
    :param product_page_data: json data of a product page
    :return: string
    """

    return product_page_data['price_inr']



def get_product_url(product_page_data):
    """
    get product price
    :param product_page_data: json data of a product page
    :return: string
    """

    url = product_page_data['url']
    updated_url = 'https://www.nicobar.com'+url
    return updated_url



def get_next_parent_page_link():
    """
    get the next page containing catalog of product..in real life this is the page 2,3,4 of the search result
    @:param parent_link: string: http link
    :returns : list: string : is a web link
    """

    page_linkss = ['https://www.nicobar.com/myapi/search/?category_shop=Women+%3E+Kurtas+%26+Tunics&currency=INR&format=json&page=1&seq_type=False&sort_by=popularity_desc&source=plp',\
                  'https://www.nicobar.com/myapi/search/?category_shop=Women+%3E+Kurtas+%26+Tunics&currency=INR&format=json&page=2&seq_type=False&sort_by=popularity_desc&source=plp']
    return page_linkss



def read_product_page_data(link):
    """
    get all values from a product page data
    :param link:string: http link
    :return:string
    """
    json_data = get_page_json(link)
    product_title = get_product_title(json_data)
    product_price = get_product_price(json_data)
    product_url = get_product_url(json_data)
    print(['Product link : '+str(product_url)+', Product title : '+str(product_title)+', Product price : '+str(product_price)])
    return (['Product link : '+str(product_url)+', Product title : '+str(product_title)+', Product price : '+str(product_price)])



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
                f.write("\t".join(map(str,individual_product))+"\n")


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
    all_search_page_links = get_next_parent_page_link()
    #for link in all_search_page_links:
        #create_file_ifnotexist(link)
    with Pool(2) as p:
        p.map(full_data_search_page, all_search_page_links)



if __name__ == '__main__':
    #PROXY_LIST = read_proxy_file()
    PARENT_LINK = 'https://www.nicobar.com/myapi/search/?category_shop=Women+%3E+Kurtas+%26+Tunics&currency=INR&format=json&page=1&seq_type=False&sort_by=popularity_desc&source=plp'
    get_all_product_data(PARENT_LINK)
