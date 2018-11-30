'''
Flipkart's product info collector
'''

# Importing libraries
import requests
import re
import random
from bs4 import BeautifulSoup
import pandas as pd
import logging
from fake_useragent import UserAgent
from multiprocessing import Pool
import os


def get_page_soup(link):
    """
    get the bs4 soup of a page
    :param link:string: http link
    :return: bs4 soup
    """
    product_link_open = requests.get(link, headers=headerrs(), proxies=proxies())
    print(product_link_open.status_code)
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
        status = requests.get("https://www.flipkart.com", headers=headerrs(), proxies={'http': ip}, timeout=0.5)
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
    kurti_page = requests.get(search_page_link, headers=headerrs(), proxies=proxies())
    kurti_soup = BeautifulSoup(kurti_page.content, 'lxml')
    all_kurti_links = kurti_soup.find_all("a")
    for each_kurti_link in all_kurti_links:
        link = each_kurti_link.get("href")
        pattern = re.compile('\/[a-z0-9_\-]+\/p\/[a-z0-9]+')
        try:
            result = pattern.findall(link)
            if result:
                result = ''.join(result)
                updated_result = 'https://www.flipkart.com'+result
                get_links.append(updated_result)
        except TypeError:
            pass
    return list(set(get_links))
                

def get_product_title(product_page_soup):
    """
    get each product title
    :param product_page_soup: bs4 soup: soup of a product page
    :return: string: product name
    """
    productname = product_page_soup.find("div", {'class' : '_29OxBi'})
    return productname.find("span", {'class' : '_35KyD6'}).text.strip()



def get_next_parent_page_link(parent_link):
    """
    get the next page containing catalog of product..in real life this is the page 2,3,4 of the search result
    @:param parent_link: string: http link
    :returns : list: string : is a web link
    """

    page_linkss = []
    kurti_page = requests.get(parent_link, headers=headerrs(), proxies=proxies())
    kurti_soup = BeautifulSoup(kurti_page.content, 'lxml')
    total_page = kurti_soup.find("div", {'class' : '_2zg3yZ'})
    pages = total_page.find("span").text.strip()
    num_of_page = pages.replace("Page", "")
    num_of_pages = ''.join(num_of_page).replace("of", "")
    num_of_pages = re.sub(',','',num_of_pages)
    num_of_pages = re.split('[\s]', num_of_pages)
    num_of_pages = int(max(num_of_pages))
    for i in range(1, 3):
        link = 'https://www.flipkart.com/women/kurtas-kurtis/pr?sid=2oq%2Cc1r%2C3pj%2Cua6&page='+str(i)
        linkz = requests.get(link, headers=headerrs(), proxies=proxies())
        if str(linkz.status_code) == '200':
            page_linkss.append(link)
        else:
            pass
    return page_linkss




def read_product_page_data(link):
    """
    get all values from a product page data
    :param link:string: http link
    :return:string
    """

    try:
        soup = get_page_soup(link)
        product_title = get_product_title(soup)
        print([product_title])
        return([link, product_title])
    except Exception as e:
        logging.error(str(e), exc_info=1)
        LEFT_OVER_LINK.append(link)
        print(link)


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
                f.write(",".join(map(str, individual_product))+"\n")


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
    
    
    

if __name__ == '__main__':
    PROXY_LIST = read_proxy_file()
    PARENT_LINK = 'https://www.flipkart.com/women/kurtas-kurtis/pr?sid=2oq%2Cc1r%2C3pj%2Cua6&page=1'
    #get_product_link_from_page(PARENT_LINK)
    print(get_next_parent_page_link(PARENT_LINK))
    
