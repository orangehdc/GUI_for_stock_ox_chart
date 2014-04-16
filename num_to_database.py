# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 13:14:01 2014
input : stock_number
@author: Administrator
"""

import urllib2, csv, sqlite3

def write_csv(csvfile,stock_number):
    print'success'
    output = open('D:/demo/stock_data/'+stock_number+'.csv','wb')
    output.write(csvfile.read())
    output.close()

def set_data(stock_number):
    site1="http://table.finance.yahoo.com/table.csv?s="
    
    #csvfile = urllib2.urlopen(site)
    try:
        csvfile = urllib2.urlopen(site1+stock_number+'.sz')
    except urllib2.HTTPError,e:
        try:    
            csvfile = urllib2.urlopen(site1+stock_number+'.ss')
        except urllib2.HTTPError,f:    
            print f
        else:
            write_csv(csvfile,stock_number)
    else:
        write_csv(csvfile,stock_number)
    
#-----------------------------------------------------------
    csvfile = file('D:/demo/stock_data/'+stock_number+'.csv', 'rb')
    reader = csv.reader(csvfile)
    reader=list(reader)
    #print type(reader)
    batchdata=[tuple(line) for line in reader]
    csvfile.close()
    
    #Info=('Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close')
    del batchdata[0]#删除文字栏，只保留数据列表
#-----------------------------------------------------------
    conn=sqlite3.connect("D:\\demo\\my_db.db")
    table_name='stock'+stock_number+' '
    sql = "CREATE TABLE IF NOT EXISTS "+table_name+\
    "( my_Date date, Open real, High real, Low real, Close real, Volume INTEGER, Adj_Close real)" 
    conn.execute(sql)
    cs = conn.cursor()
    sql = "insert or replace INTO "+table_name+" values (?,?,?,?,?,?,?) "
    cs.executemany(sql,batchdata[0:120])
    conn.commit()  #将加入的记录保存到磁盘
    cs.close()
    conn.close()

if __name__ == "__main__":
    stock_number='000776'
    set_data(stock_number)