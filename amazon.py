'''
Amazon product comment collector
'''
# Importing libraries
import urllib.request as urllib2
import re
import sys
from bs4 import BeautifulSoup

def kurti_read():
    '''
    Parse the url and return a html to the variable page
    '''
    product_kurti = 'https://www.amazon.in/kurti-Ethnic-Wear-Women/s?ie=UTF8&page=1&rh=n%3A1571271031%2Ck%3Akurti'
    
    kurti_page = urllib2.urlopen(product_kurti)

    return kurti_page

parent_link = kurti_read()

get_links = []
def get_product_link_from_page(parent_link):
    '''
    write a fucntion to read the given page and return product link from the page in a list
    '''
    get_links = []
    kurti_soup = BeautifulSoup(parent_link, 'lxml')
    all_kurti_links = kurti_soup.find_all("a")
    for each_kurti_link in all_kurti_links:
        link = each_kurti_link.get("href")
        print(link)
        pattern = re.compile('https://www.amazon.in/.*/dp.*')
        try:
            result = pattern.findall(link)
            if result:
                get_links.append(result[0])
        except TypeError:
            pass
    return(get_links)


print(get_product_link_from_page(parent_link))
