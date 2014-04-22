# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 10:15:59 2014

@author: Administrator
"""
import sqlite3
def param(table_name):
    conn=sqlite3.connect("D:\\demo\\my_db.db")
    cs = conn.cursor()
    sql="SELECT * FROM "+table_name
    cs.execute( sql)
    recs = cs.fetchall()
    #Info=('Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close')       
    current = recs[0][1]
    smallest=min([line[3] for line in recs])
    
    if 0.02*current>=0.1:
        unit=int(10*(0.02)*(current))*0.1
    else:
        unit=int(50*(0.02)*(current))*0.02

    start_price=int(smallest-unit)
    return start_price, unit