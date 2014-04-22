# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 19:01:17 2014

@author: Administrator
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys, os
import Stack_QGraphsView
import get_stock_name
import num_to_database
import sqlite3
#import draw_kline
import draw_kline_para
import get_start_and_unit
#解决打包的中文出错问题
reload(sys)
sys.setdefaultencoding( "utf-8" )#if not, fetch should use gbk
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class OptionWidget(QDialog):
    def __init__(self,parent=None):
        super(OptionWidget,self).__init__(parent) 
        font=QFont(self.tr("黑体"),12)
        QApplication.setFont(font)
        self.setWindowTitle(self.tr(u"股票OX图绘制程序"))                
        #初始化数据库---------------------------        
        conn=sqlite3.connect("D:\\demo\\my_db.db")
        sql = "CREATE TABLE IF NOT EXISTS name_total ( number char , name nchar, start real, unit real )" 
        conn.execute( sql )
        sql="create unique index if not exists idex on name_total(number,name,start,unit)"
        conn.execute(sql)        
        cs = conn.cursor()
        cs.execute( "insert or replace INTO name_total ( number,name,start,unit ) values('000000','Welcome!',0,0)")
        conn.commit()  #将加入的记录保存到磁盘

        #初始化列表---------------------------------
        self.listWidget=QListWidget()
        self.listWidget.insertItem(0,self.tr("000000"))
        cs.execute( "SELECT * FROM name_total ")#打开数据表
        recs = cs.fetchall()#取出所有记录
        for stock_num,stock_name,tmp1,tmp2 in recs:
            if stock_num!='000000':
                self.listWidget.insertItem(0,self.tr(stock_num))
        cs.close()
        conn.close()
        #---------------------------------------------
        addPushButton=QPushButton(self.tr(u"添加新股票"))
        delPushButton=QPushButton(self.tr(u"移出股票"))
        showPushButton=QPushButton(self.tr(u"显示OX图"))

        buttonLayout=QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(addPushButton)
        buttonLayout.addWidget(delPushButton)
        buttonLayout.addWidget(showPushButton)
        
        mainLayout=QHBoxLayout(self)
        mainLayout.setMargin(10)
        mainLayout.setSpacing(6)        

        leftLayout=QVBoxLayout()        
        leftLayout.addLayout(buttonLayout)
        leftLayout.addWidget(self.listWidget) 
        mainLayout.addLayout(leftLayout)


        right_Layout=QGridLayout()

        self.Information1=QLabel(self.tr('Welcome!'))        
        self.Information2=QLabel(self.tr('最小单位'))
        self.Information3=QLabel(self.tr('起始价格'))
        self.unitLabel=QLabel(" ")
        self.unitLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.priceLabel=QLabel(" ")
        self.priceLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        unitButton=QPushButton(u'修改')
        priceButton=QPushButton(u'修改')
        self.connect(unitButton,SIGNAL("clicked()"),self.slotUnit)
        self.connect(priceButton,SIGNAL("clicked()"),self.slotPrice)

        right_Layout.addWidget(self.Information1,0,0,1,2)#实例12 1，2代表面积
        
        right_Layout.addWidget(self.Information2,1,0)
        right_Layout.addWidget(self.unitLabel,1,1)
        right_Layout.addWidget(unitButton,1,2)
        
        right_Layout.addWidget(self.Information3,2,0)
        right_Layout.addWidget(self.priceLabel,2,1)
        right_Layout.addWidget(priceButton,2,2)
        
        mainLayout.addLayout(right_Layout)                         
      
        self.stockNumber=QLabel("000000")              
       
        self.connect(addPushButton,SIGNAL("clicked()"),self.add_Item)
        self.connect(delPushButton,SIGNAL("clicked()"),self.del_Item)
        self.connect(showPushButton,SIGNAL("clicked()"),self.show_Item)
        
        self.connect(self.listWidget, SIGNAL("currentRowChanged(int)"),
                     self.refresh)
                  
        self.setGeometry(100, 50, 100, 300)
        self.setLayout(mainLayout)
    

    def slotUnit(self):
        my_unit,ok=QInputDialog.getDouble(self,self.tr("最小单位"),
                                          self.tr("请输入最小单位:"),
                                          float(self.unitLabel.text()),0,2300.00)
        if ok:
            self.unitLabel.setText(str(my_unit))
            
            row = self.listWidget.currentRow()
            the_text = self.listWidget.item(row)
            stock_num=str(the_text.text() )
            conn=sqlite3.connect("D:\\demo\\my_db.db")
            cs = conn.cursor()
            sql='update name_total set unit='+str(my_unit)\
            + ' where number='+"'"+str(stock_num)+"'"
            print sql
            cs.execute(sql)
            conn.commit()  #将加入的记录保存到磁盘
            cs.close()
            conn.close()
            
            
    def slotPrice(self):
        my_price,ok=QInputDialog.getDouble(self,self.tr("起始价格"),
                                          self.tr("请输入起始价格:"),
                                          float(self.priceLabel.text()),0,2300.00)
        if ok:            
            self.priceLabel.setText(str(my_price))
            
            row = self.listWidget.currentRow()
            the_text = self.listWidget.item(row)
            stock_num=str(the_text.text() )
            conn=sqlite3.connect("D:\\demo\\my_db.db")
            cs = conn.cursor()
            sql='update name_total set start='+str(my_price)\
            + ' where number='+"'"+str(stock_num)+"'"
            print sql
            cs.execute(sql)
            conn.commit()  #将加入的记录保存到磁盘
            cs.close()
            conn.close()
            
    def add_Item(self):
        '''用getInterger'''
        num,ok=QInputDialog.getText(self,self.tr(u"股票代码"),
                   self.tr(u"请输入股票代码:"),
                  QLineEdit.Normal,self.stockNumber.text())
        if ok :
            self.listWidget.insertItem(0,self.tr(str(num)))
        '''0表示插入位置'''
        
        stock_num=str(num)
        stock_name=get_stock_name.get_name(stock_num)
        print stock_name
        conn=sqlite3.connect("D:\\demo\\my_db.db")
        cs = conn.cursor()
        batch=[(stock_num, unicode(stock_name, "gbk") ,0,0 )] 
        cs.executemany( "insert or replace INTO name_total values (?,?,?,?) ",batch)
        conn.commit()  #将加入的记录保存到磁盘
        
        if stock_name!="not available":
            num_to_database.set_data(stock_num)
            table_name = 'stock'+str(num)
            start_price,unit=get_start_and_unit.param(table_name)
            #print start_price
            sql='update name_total set start='+str(start_price)\
            +',unit='+str(unit)+ ' where number='+"'"+str(stock_num)+"'"
            print sql
            cs.execute(sql)
            conn.commit()  #将加入的记录保存到磁盘
        cs.close()
        conn.close()
            
    def del_Item(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.item(row)
        if item is None:
            return
        reply = QMessageBox.question(self, u"移出股票 " ,
                        u"确认移出该股票 %s ?" % (
                        item.text()),
                        QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.Yes:
            item = self.listWidget.takeItem(row)            
            conn=sqlite3.connect("D:\\demo\\my_db.db")
            cs = conn.cursor()
            sql="DELETE FROM name_total WHERE number='"+str(item.text())+"'"
            #print sql
            cs.execute(sql)
            sql="DROP TABLE IF EXISTS stock"+str(item.text())
            cs.execute(sql)
            conn.commit()  #将加入的记录保存到磁盘
            cs.close()
            conn.close()
            del item
    
    def show_Item(self):        
        row = self.listWidget.currentRow()
        item = self.listWidget.item(row)      
        
        table_name = 'stock'+str(item.text() )        
        jpg_name = table_name+'.png'
    
        unit= float(self.unitLabel.text())
        start=float(self.priceLabel.text())
        
        stock_num=str(item.text() )
        conn=sqlite3.connect("D:\\demo\\my_db.db")
        cs = conn.cursor()
        query= "SELECT * FROM name_total WHERE number ='"+ stock_num+"'"
        cs.execute(query )
        result=cs.fetchall()        
        the_name=(result)[0][0]
        print the_name
        
        draw_kline_para.draw(table_name,start,unit,the_name)
        dialog = QDialog()
        small_layout=QVBoxLayout()
        #---------------------------               
        my_widget=Stack_QGraphsView.Graph_view(jpg_name)
        small_layout.addWidget(my_widget)
        dialog.setLayout(small_layout)
        dialog.resize(1200,750)
        #dialog.setAttribute(Qt.WA_DeleteOnClose)显示K线图
        dialog.exec_()
        
    def refresh(self,row=None):
        the_text = self.listWidget.item(row)
        stock_num=str(the_text.text() )
        conn=sqlite3.connect("D:\\demo\\my_db.db")
        cs = conn.cursor()
        query= "SELECT * FROM name_total WHERE number ='"+ stock_num+"'"

        cs.execute(query )
        result=cs.fetchall()
        
        the_name=(result)[0][1].decode('utf-8')               
        start_price=result[0][2]
        unit=result[0][3]

        self.Information1.setText(the_name )        
        self.unitLabel.setText(str(unit))
        self.priceLabel.setText(str(start_price))
        
'''还是用窗口显示图片比较好'''            
        
if __name__ == "__main__":
    file_path="D:\\demo"
    print file_path
    isExists=os.path.exists(file_path)
    print isExists
    if not isExists:    
        os.mkdir(file_path)
        os.mkdir(file_path+"\\jpg")
        os.mkdir(file_path+"\\stock_data")
    app=QApplication(sys.argv)
    main=OptionWidget()
    #main.insert_newItem(50000)
    #main=MyMainWindow()
    main.show()
    app.exec_()