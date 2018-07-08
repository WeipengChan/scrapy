# -*- coding: utf-8 -*-
import scrapy
import re
import time
import os
import random
from urllib.parse import quote_plus, urlparse, parse_qs
import requests
import cchardet
# import logging

# logging.getLogger("urllib3").setLevel(logging.WARNING)
# logging.getLogger("chardet").setLevel(logging.WARNING)
# logging.getLogger("requests").setLevel(logging.WARNING)
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
# LOGGER = logging.getLogger('magic_google')

BLACK_DOMAIN = ['www.google.gf', 'www.google.io', 'www.google.com.lc']

DOMAIN = 'www.google.com'
URL_SEARCH = "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=1"
URL_NUM = "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=1&num={num}"
URL_NEXT = "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=1&num={num}&start={start}"

class ToGmailpider(scrapy.Spider):
    name = "gmail1"
    page = 0
    start_urls = [
        'https://www.google.com/search?source=hp&ei=4A4pW_CQKpC08AO_3JKABA&q=gmail.com&oq=gmail.com'
    ]

    def parse(self, response):


        page = self.page + 1
       # print(page)
        mlist = response.xpath("//span[@class='st']//text()").extract()

        str = "".join(mlist)
        r = re.findall(r"[0-9a-zA-Z_]{0,19}@gmail.com",str)
       # print(r)

        # for quote in response.css("div.quote"):
        yield {
            'page': page,
            'mails': r
            }

        # pn =  response.xpath("//a[@class='pn']/@href").extract_first()
        # print("pn",pn)

        # pnnext =  response.xpath("//a[@id='pnnext']/@href").extract_first()
        # print("pnnext",pnnext)
        # if pnnext is not  None:
        self.page = int(page)
        print(self.page)
        self.search_page("gmail.com",language=None , num=self.page)

        domain = self.get_random_domain()
        print(domain)

        url = URL_NUM
        url = url.format(
                    domain=domain, language=None, query=quote_plus("gmail.com"), num=self.page)
        url = url.replace('hl=None&', '')
        # Add headers
        print("getting",url)
        yield scrapy.Request(url)
        #yield scrapy.Request( "https://" + domain + pnnext)

        #self.search_page("gmail.com",language=None,start=1,pause=2)



    def search_page(self, query, language=None, num=None, start=0, pause=2):
        """
        Google search
        :param query: Keyword
        :param language: Language
        :return: result
        """
        # time.sleep(pause)
        domain = self.get_random_domain()
        print(domain)
        if start > 0:
            url = URL_NEXT
            url = url.format(
                domain=domain, language=language, query=quote_plus(query), num=num, start=start)
        else:
            if num is None:
                url = URL_SEARCH
                url = url.format(
                    domain=domain, language=language, query=quote_plus(query))
            else:
                url = URL_NUM
                url = url.format(
                    domain=domain, language=language, query=quote_plus(query), num=num)
        if language is None:
            url = url.replace('hl=None&', '')
        # Add headers
        print("getting",url)
        yield scrapy.Request(url)




    def get_random_domain(self):
        """
        Get a random domain.
        :return: Random user agent string.
        """
        domain = random.choice(self.get_data('all_domain.txt', DOMAIN))
        if domain in BLACK_DOMAIN:
            self.get_random_domain()
        else:
            return domain

    def get_data(self, filename, default=''):
        """
        Get data from a file
        :param filename: filename
        :param default: default value
        :return: data
        """
        root_folder = os.path.dirname(__file__)
        user_agents_file = os.path.join(
            os.path.join(root_folder, 'data'), filename)
        try:
            with open(user_agents_file) as fp:
                data = [_.strip() for _ in fp.readlines()]
        except:
            data = [default]
        return data