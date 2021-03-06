'''
Amazon product info collector
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
        status = requests.get("http://google.com", headers=headerrs(), proxies={'http': ip}, timeout=0.5)
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
        pattern = re.compile('https:\/\/www.amazon.in\/[A-Za-z0-9_\-]+\/dp\/[A-Z0-9]+')
        try:
            result = pattern.findall(link)
            if result:
                get_links.append(result[0])
        except TypeError:
            pass
    return list(set(get_links))


def get_product_title(product_page_soup):
    """
    get each product title
    :param product_page_soup: bs4 soup: soup of a product page
    :return: string: product name
    """
    productname = product_page_soup.find("div", {'id': 'titleBlock'})
    return productname.find("span", {'id': 'productTitle'}).text.strip()


def get_product_rating(product_page_soup):
    """
    get each product rating
    :param product_page_soup: bs4 soup: soup of a product page
    :return: string: product rating
    """
    each_product_rating = product_page_soup.find("div", {'id': 'averageCustomerReviews'})
    try:
        return each_product_rating.find("span", {'class': 'a-icon-alt'}).text.strip()

    except AttributeError:
        return None


def get_product_review(product_page_soup):
    """
    get product total number of review
    :param product_page_soup: bs4 soup: soup of a product page
    :return:string
    """
    each_product_review = product_page_soup.find("div", {'id': 'averageCustomerReviews'})
    return each_product_review.find("span", {'class': 'a-size-base'}).text.strip()


def get_product_price(product_page_soup):
    """
    get product total number of review
    :param product_page_soup: bs4 soup: soup of a product page
    :return: string
    """

    each_product_price = product_page_soup.find("div", {'id': 'desktop_unifiedPrice'})
    prices = each_product_price.find("span", {'class': 'a-size-medium a-color-price'})
    return prices.text.strip()


def get_next_parent_page_link(parent_link):
    """
    get the next page containing catalog of product..in real life this is the page 2,3,4 of the search result
    @:param parent_link: string: http link
    :returns : list: string : is a web link
    """

    page_linkss = []
    # parent_link = 'https://www.amazon.in/kurti-Clothing-Accessories/s?ie=UTF8&page=1&rh=n%3A1571271031%2Ck%3Akurti'
    kurti_page = requests.get(parent_link, headers=headerrs(), proxies=proxies())
    kurti_soup = BeautifulSoup(kurti_page.content, 'lxml')
    bottom_next_page_bar = kurti_soup.find("div", {'id': 'centerBelowMinus'})
    last_page = int(bottom_next_page_bar.find("span", {'class': 'pagnDisabled'}).text.strip())
    for i in range(1, last_page+1):
        link = 'https://www.amazon.in/s/ref=sr_pg_2?rh=n%3A1571271031%2Ck%3Ahandloom+saree&page={}&keywords=handloom+saree&ie=UTF8&qid=1543831229'.format(i)
        page_linkss.append(link)
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
        product_price = get_product_price(soup)
        product_rating = get_product_rating(soup)
        product_review = get_product_review(soup)
        print([product_title, product_price, product_rating, product_review])
        return [link, product_title, product_price, product_rating,
                product_review]
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
    #for link in all_search_page_links:
    #    create_file_ifnotexist(link)
    with Pool(50) as p:
        p.map(full_data_search_page, all_search_page_links)


def convert_to_dataframe(list_of_list):
    """
    :param list_of_list: ["product_title","product_price","product_rating","product_review"]
    :return: pandas.DataFame
    """
    header = ["product_title", "product_price", "product_rating", "product_review"]
    df = pd.DataFrame(list_of_list, columns=header)
    return df


if __name__ == '__main__':
    LEFT_OVER_LINK = []
    PROXY_LIST = read_proxy_file()
    PARENT_LINK = 'https://www.amazon.in/s/ref=sr_pg_2?rh=n%3A1571271031%2Ck%3Ahandloom+saree&page=1&keywords=handloom+saree&ie=UTF8&qid=1543831229'
    get_all_product_data(PARENT_LINK)
