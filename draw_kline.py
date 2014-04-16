# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 19:45:23 2014
input table_name, start_price, unit
@author: Administrator
"""
import numpy
import matplotlib
import sqlite3
matplotlib.use('Agg')
''' Very important! It must be put immediately after import matplotlib!'''
import matplotlib.pyplot as plt

def process(line):
    return (line[0],line[2],line[3],(line[4]-line[1])>0)
    #        date     max     min      up_or_down


def draw(table_name):
    
    conn=sqlite3.connect("D:\\demo\\my_db.db")
    cs = conn.cursor()
    sql="SELECT * FROM "+table_name
    cs.execute( sql)
    recs = cs.fetchall()
    #Info=('Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close')       
    current = recs[0][1]
    biggest=max([line[2] for line in recs])
    smallest=min([line[3] for line in recs])
    
    if 0.02*current>=0.1:
        unit=int(10*(0.02)*(current))*0.1
    else:
        unit=int(50*(0.02)*(current))*0.02

    start_price=int(smallest-unit)
    recs.reverse()
    for line in recs:
        if line[5]==0:
            recs.remove(line)
            
    batchdata=[process(line) for line in recs]
    
    #Info=('Date', 'High', 'Low', up_or_down)
    #---------------初始化----------------
    compress=[list(batchdata[0])]
    previous=compress[len(compress)-1]
    for line in batchdata:
        if line[3]==previous[3]:#走势不变
            if line[2]<previous[2]: #比小的更小
                compress[len(compress)-1][2]=line[2]
            if line[1]>previous[1]: #比大的更大
                compress[len(compress)-1][1]=line[1]
        else:
            compress.append(list(line))
        previous=compress[len(compress)-1]
    '''    
    for line in compress:
    print line[0:3]
    '''
    '''
    #---过滤无效下跌或无效上涨----------------------
    for line in compress:
        if abs(line[3])<unit:
            compress.remove(line)    

    #--------再压缩------------------- 
    temp=compress   
    compress=[temp[0],]
    previous=compress[len(compress)-1]
    for line in temp:
    if line[3]*previous[3]>0:#走势不变
        if line[2]<previous[2]: #比小的更小
            compress[len(compress)-1][2]=line[2]
        if line[1]>previous[1]: #比大的更大
            compress[len(compress)-1][1]=line[1]
    else:
        compress.append(list(line))
    previous=compress[len(compress)-1]
    '''
    #-------添加X的坐标-----------------
    for i,line in enumerate(compress):
        line.append(i+1)    
        #Info=('Date', 'High', 'Low', up_or_down, x_pos)     
    def gene_date_list(line):
        return line[0][5:10]#前面的2014-不要，只要日期xx-xx
        
    def gene_x_list(line):
        return line[4]

    up_list=[]
    down_list=[]
    for line in compress:  
        if line[3]==True:#上涨
            up_list.append(line)
        else:
            down_list.append(line)
        #Info=('Date', 'High', 'Low', up_or_down, x_pos) 
    #----------生成日期坐标---------------------
    date_list=[gene_date_list(line) for line in up_list]
    x_list=[gene_x_list(line) for line in up_list]
    
    def list_to_point(line,x,y):
        startt=int((line[2]-start_price)/unit)
        endd=int((line[1]-start_price)/unit)    
        for i in range(startt,endd+1):
            x.append(line[4])
            y.append(start_price+i*unit)
            
    x1=[]
    y1=[]
    x2=[]
    y2=[]
        
    for line in up_list:
        list_to_point(line,x1,y1)
    for line in down_list:
        list_to_point(line,x2,y2)

    fig = plt.figure()

    ax = fig.gca()
    biggest=biggest+2*unit
    ax.set_ylim([start_price,biggest])
    ax.set_xticks(numpy.arange(0,len(x_list)+2,1))
    ax.set_yticks(numpy.arange(start_price,biggest,unit))
    #plt.scatter(x,y)
    plt.xticks(x_list, date_list)
    plt.plot(x1, y1, 'x',mfc='none',markersize=10)
    plt.plot(x2, y2, 'o',mfc='none',markersize=10)
    '''
    http://stackoverflow.com/questions/6390393/matplotlib-make-tick-labels-font-size-smaller
    '''
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(10) 
        tick.label.set_rotation('vertical')

    plt.grid()
    plt.show()
    fig.set_size_inches(13,7)#good
    the_path='D:/demo/jpg/'+table_name+'.png'
    plt.savefig(the_path, format='png')
    
        
if __name__ == "__main__":        
    table_name='stock'+'600805'    
    draw(table_name)