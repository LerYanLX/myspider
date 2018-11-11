"""
  作者：wanderees
  时间： 2018-7-29
  注：amazon对爬取进行了限制，爬不完全部就会被BAN。可添加代理IP池进行爬取。
"""
#coding=utf-8
import re
import requests
from urllib import request
import urllib
from bs4 import BeautifulSoup
import time
from urllib import error
import chardet
from html.parser import HTMLParser

#'https://www.amazon.cn/s/ref=lp_116087071_pg_2?rh=n%3A116087071&page=2&ie=UTF8&qid=1534933293'
def Get_content(url):         #获得网页源码
    headers = {
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'referer': 'https://www.amazon.cn/Kindle%E5%95%86%E5%BA%97/b/ref=sa_menu_top_kindle_l1_store?ie=UTF8&node=116087071'
    }
    cookies = {'session-id': '457-2640116-4797625',
               'session-id-time': 'd8vuZaLT9TPRWSBAY11rqZfbV0M.sA4VcU65%2FV0UVWPR3b04xfV43Z%2BSDztHZFUtdi28SdY',
               'session-token': '\"H69qBnZUaiP1CX+1Or8WCi311x8s+086M0BhP+xCL+0+c4BPg7kP9l5p5PgC5F7E1Sl2YEkcfdNtMyW/xOXk2TIwmDqRuLaNbZnGLxSeTLYqq1Z20OEnzg1qk2Ubw00rHJYAAfnaLTsxzH2pB3q2At/skzTtlll44S05c4qjyALi67HMB5mbdmryhXb/+eIA0PEqkTxGIm0NXXK5fZ5pGuu6nuL0JAqvafFiUPe8cElSokBthJpTMg==\"',
               'ubid-acbcn': '457-5554500-4615301',
               'x-wl-uid': '1HM3D2YCzhfjaB0H1JIi+giqMOe3sEfviDAd8WM2pRFEk9782bYQNrSOXsOAqHX/c84MBxXxIin0=',
               'csm-hit': 'tb:9C8WN9ZC7TDGPWAN4CK6+s-EV1KH9VW5ECH2DVT29QW|1534933968298&adb:adblk_no',
               'floatingBannerOnGateway': 'floatingBannerOnGateway'}
    s = requests.session()
    r = s.get(url,
              headers=headers, cookies=cookies, timeout=40)
    # save_html(r.text.encode('GB18030'))
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def Get_book_url(url_list):          #获得图书的URL列表
    href_list = []
    for url in url_list:
        soup = Get_content(url)
        all = re.findall('<div class="a-row s-result-list-parent-container"(.+)</div>', str(soup), re.S)
        href = re.findall(
            r'<a class="a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal" href="(.+?)" target="_blank"',
            str(all), re.S)
        href_list.append(href)
    return href

def Get_price(url_list):        #获得图书价格
    title_list = []
    price_list = []
    jinzhuang_list = []
    pinzhuang_list = []
    for url in url_list:
        content = Get_content(url)
        title = content.find(name='span', attrs={'id': 'ebooksProductTitle'}).get_text()
        title_list.append(title)
        print(title_list)
        first_price = content.find(name='span', attrs={'class': 'a-color-price'}).get_text()
        price_all = content.find(name='ul', attrs={'class': 'a-unordered-list a-nostyle a-button-list a-horizontal'}).get_text()
        price_content = str(price_all).replace('\n','').replace('\r','').replace('\t','')
        print(price_content)
        if "平装" in str(price_content):          #判断有无平装价格，没有就添加nothong
            pinzhuang_price = re.findall(r'.+?平装.+?(￥\d+.\d+).+?', price_content, re.S)
            pinzhuang_list.append(pinzhuang_price)
        elif "平装" not in str(price_content):     
            pinzhuang_list.append('Nothing')
        if "精装" in str(price_content):     #判断有无精装价格，没有就添加nothing
            jinzhuang_price = re.findall(r'.+?精装.+?(￥\d+.\d+).+?', price_content, re.S)
            jinzhuang_list.append(jinzhuang_price)
        elif "精装" not in str(price_content):
            jinzhuang_list.append('Nothing')
        kindle_price = re.findall(r'Kindle电子书.+?(￥\d+.\d+).+?', price_content)
    print(kindle_price)
    print(jinzhuang_list)
    print(pinzhuang_list)
#url = ['https://www.amazon.cn/s/ref=lp_116087071_pg_2?rh=n%3A116087071&page=2&ie=UTF8&qid=1534933293','https://www.amazon.cn/s/ref=lp_116087071_pg_3?rh=n%3A116087071&page=3&ie=UTF8&qid=1534933293']
url_list = []
url = 'https://www.amazon.cn/s/ref=lp_116087071_pg_2?rh=n%3A116087071&page=2&ie=UTF8&qid=1534933293'
x = list(url)
for page in range(2,401):     #总共400页，但是由于亚马逊的反爬机制，一个只能爬几十页就会被BAN,添加代理IP池即可解决这种情况。
    x[-24] = '%s' % page
    x[44] = '%s' % page
    list1 = ''.join(x)
    url_list.append(list1)
print(url_list)
Get_book_url(url_list)

#r'<span class="a-color-price">|<span class="a-size-base a-color-price a-color-price">(.+?)</span>'
