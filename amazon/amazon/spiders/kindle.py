# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonItem
from bs4 import BeautifulSoup
import re


class KindleSpider(scrapy.Spider):
    name = 'kindle'
    allowed_domains = ['amazon.cn']
    start_urls = ['https://www.amazon.cn/s/ref=lp_116087071_pg_2?rh=n%3A116087071&page=2&ie=UTF8&qid=1536027113']

    def parse(self, response):       #从start_urls的response里获得下一页链接
        item = AmazonItem()
        next_href = response.xpath('//*[@id="pagnNextLink"]/@href').extract()       #//*[@id="pagn"]/span[4]/a     //*[@id="pagn"]/span[4]/a
        href = str(next_href).replace('\'','')
        group_url = response.urljoin(href.replace('[','').replace(']',''))        #//*[@id="pagnNextLink"]/@href
        print(group_url)
        book_url = response.xpath('//*[@id="s-results-list-atf"]/li/div/div/div/div[2]/div[1]/div[1]/a/@href').extract()
        item['group_url'] = book_url  # //*[@id="result_16"]/div/div[2]/div/div[2]/div[1]/div[1]/a  id="s-results-list-atf"
        for url in book_url:
            yield scrapy.Request(url, callback=self.parse_price)  # 回调进入书籍详情页爬取价格信息
        print("啊实打实大撒时候的噶湿度就是大家好gas等哈说大家看过")
        yield scrapy.Request(group_url, callback=self.parse)  # 回调进入parse函数获取下一页
        pass

    '''def parse_book(self,response):         #获取下一页链接和书籍详情页的链接
        item = AmazonItem()
        next_href = response.xpath('//*[@id="pagn"]/span[3]/a/@href').extract()
        href = str(next_href).replace('\'', '')
        group_url = response.urljoin(href.replace('[', '').replace(']', ''))
        book_url = response.xpath('//*[@id="s-results-list-atf"]/li/div/div/div/div[2]/div[1]/div[1]/a/@href').extract()
        item['group_url'] = book_url  #//*[@id="result_16"]/div/div[2]/div/div[2]/div[1]/div[1]/a  id="s-results-list-atf"
        for url in book_url:
            yield scrapy.Request(url,callback=self.parse_price)    #回调进入书籍详情页爬取价格信息
        return scrapy.Request(group_url, callback=self.parse)       #回调进入parse函数获取下一页'''

    def parse_price(self,response):            #获取书籍详情页价格信息的函数
        item = AmazonItem()
        content = BeautifulSoup(response.body, 'html.parser')
        try:
            title = content.find(name='span', attrs={'id': 'ebooksProductTitle'}).get_text()
            item['book_name'] = title
            first_price = content.find(name='span', attrs={'class': 'a-color-price'}).get_text()
            price_all = content.find(name='ul',attrs={'class': 'a-unordered-list a-nostyle a-button-list a-horizontal'}).get_text()
            price_content = str(price_all).replace('\n', '').replace('\r', '').replace('\t', '')
            if "平装" in str(price_content):
                item['pin_price'] = re.findall(r'.+?平装.+?(￥\d+.\d+).+?', price_content, re.S)
            elif "平装" not in str(price_content):
                item['pin_price'] = 'Nothing'
            if "精装" in str(price_content):
                item['jin_price'] = re.findall(r'.+?精装.+?(￥\d+.\d+).+?', price_content, re.S)
            elif "精装" not in str(price_content):
                item['jin_price'] = 'Nothing'
            item['kindle_price'] = re.findall(r'Kindle电子书.+?(￥\d+.\d+).+?', price_content)
            yield item
        except:
            print('error')
#//*[@class="a-color-price"]/span   //*[@class="a-butter-inner"]/a/span[2]/span