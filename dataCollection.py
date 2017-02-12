# -*- coding: utf-8 -*-
import os
import sys
import urllib2
import requests
import re
from lxml import etree
import MySQLdb
conn = MySQLdb.connect("128.199.137.57","root","","test")
x = conn.cursor()

def Page_Info(myPage):
    '''Regex'''
    mypage_Info = re.findall(r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>', myPage, re.S)
    return mypage_Info

def New_Page_Info(new_page):
    '''Regex(slowly) or Xpath(fast)'''
    dom = etree.HTML(new_page)
    new_items = dom.xpath('//tr/td/a/text()')
    new_urls = dom.xpath('//tr/td/a/@href')
    assert(len(new_items) == len(new_urls))
    return zip(new_items, new_urls)

def Spider(url):
    i = 0
    k = 0
    y = 0
    myPage = requests.get(url).content.decode("gbk")
    myPageResults = Page_Info(myPage)
   

    i += 1
    k += 1
    y += 1
    for item, url in myPageResults:
        new_page = requests.get(url).content.decode("gbk")
        newPageResults = New_Page_Info(new_page)
        newItem = zip(*newPageResults)[0]
        newURL = zip(*newPageResults)[1]
        for j in newItem:

            ChineseEncodeResult = j.encode('utf-8')
            x.execute("""INSERT INTO wangYiDatas VALUES (%s,%s,%s)""",(k,ChineseEncodeResult,1))
            k += 1
        
        for l in  newURL:
            x.execute("""UPDATE wangYiDatas set url = %s WHERE id = %s""",(l,y))
            y += 1

        conn.commit()
        i += 1


if __name__ == '__main__':
    print "start"
    start_url = "http://news.163.com/rank/"
    Spider(start_url)
    print "end"
