# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 23:06:25 2014

@author: Administrator
"""
#!/usr/bin/env python   

import urllib2  
from HTMLParser import HTMLParser

class TitleParser(HTMLParser):
    def __init__(self):
        self.title=''
        self.readingtitle=0
        HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.readingtitle = 1
            
    def handle_data(self,data):
        if self.readingtitle:
            self.title += data
            
    def handle_endtag(self, tag):
        if tag == 'title':
            self.readingtitle = 0
            
    def gettitle(self):
        return self.title
def get_name(stock_number):   
    if stock_number=='000000':
        return 'Welcome!'    
    
    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14','Accept':'application/json'}   
    #url='http://stockdata.stock.hexun.com/'+stock_number+'.shtml'
    url='http://stock.quote.stockstar.com/'+stock_number+'.shtml'
    request = urllib2.Request(url, headers=header)
    #response = urllib2.urlopen(request)   
    try: 
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
            print e,"failed"
            return "not available"
    else:
        data = response.read()  
        fp = open('D:/demo/htmlsource.txt','w')
        #print data
        fp.write(data)
        fp.close
        fp = open('D:/demo/htmlsource.txt')
        tp = TitleParser()
        tp.feed(fp.read())
        #print "Title is:", tp.gettitle()
        temp_str = tp.gettitle()
        start=temp_str.find('\n')+1
        end = temp_str.find('(')
        #print  u'股票是'+temp_str[0:temp_str.find('(')]
        the_name=(temp_str[start:end]).replace(' ','')
        return the_name

        
if __name__ == "__main__":
    stock_number='6000999'
    print get_name(stock_number),
    #print len(get_name(stock_number))
    #print len('招商证券')
