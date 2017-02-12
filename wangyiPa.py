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


def StringListSave(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".txt"
    with open(path, "w+") as fp:
        for s in slist:
            fp.write("%s\t\t%s\n" % (s[0].encode("utf8"), s[1].encode("utf8")))

def Page_Info(myPage):
    '''Regex'''
    mypage_Info = re.findall(r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>', myPage, re.S)
    return mypage_Info

def New_Page_Info(new_page):
    '''Regex(slowly) or Xpath(fast)'''
    # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)\.html".*?>(.*?)</a></td>', new_page, re.S)
    # # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)">(.*?)</a></td>', new_page, re.S) # bugs
    # results = []
    # for url, item in new_page_Info:
    #     results.append((item, url+".html"))
    # return results
    dom = etree.HTML(new_page)
    new_items = dom.xpath('//tr/td/a/text()')
    new_urls = dom.xpath('//tr/td/a/@href')
    assert(len(new_items) == len(new_urls))
    return zip(new_items, new_urls)
    #return new_items, new_urls

def Spider(url):
    i = 0
    k = 0
    y = 0
    #print "downloading ", url
    myPage = requests.get(url).content.decode("gbk")
    # myPage = urllib2.urlopen(url).read().decode("gbk")
    myPageResults = Page_Info(myPage)
    save_path = u"网易新闻抓取"
    filename = str(i)+"_"+u"新闻排行榜"
    StringListSave(save_path, filename, myPageResults)
    i += 1
    k += 1
    y += 1
    for item, url in myPageResults:
       #print "downloading ", url
        new_page = requests.get(url).content.decode("gbk")
        # new_page = urllib2.urlopen(url).read().decode("gbk")
        newPageResults = New_Page_Info(new_page)
        #newItem = newPageResults(new_items)
        #newURL = newPageResults.new_urls
        filename = str(i)+"_"+item
        StringListSave(save_path, filename, newPageResults)
        #print newPageResults
        newItem = zip(*newPageResults)[0]
        newURL = zip(*newPageResults)[1]
        for j in newItem:
            #print j
            #print "-----"
            ChineseEncodeResult = j.encode('utf-8')
            x.execute("""INSERT INTO wangYiDatas VALUES (%s,%s,%s)""",(k,ChineseEncodeResult,1))
            k += 1
        
        for l in  newURL:
            x.execute("""UPDATE wangYiDatas set url = %s WHERE id = %s)"""%(l,y))
            y += 1

        conn.commit()

        #x.execute("""INSERT INTO wangYiDatas VALUES (%s,%s,%s)""",(i,item,url))
        i += 1
        #print item
    #conn.commit()     
        #print newItem
    #try:
        
    #except:
        #conn.rollback()
    #conn.close()    


if __name__ == '__main__':
    print "start"
    start_url = "http://news.163.com/rank/"
    Spider(start_url)
    print "end"
