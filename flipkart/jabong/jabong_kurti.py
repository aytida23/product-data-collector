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
	    status = requests.get("https://www.google.co.in", headers=headerrs(), proxies={'http': ip}, timeout=0.5)
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
        print(link)


if __name__ == '__main__':
    LEFT_OVER_LINK = []
    PROXY_LIST = read_proxy_file()
    PARENT_LINK = 'https://www.jabong.com/amp/kurtis'
    get_product_link_from_page(PARENT_LINK)
