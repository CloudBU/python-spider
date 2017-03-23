# -*- coding:utf-8 -*-
# -*- coding: utf-8 -*-

import urllib2
import sys
import re
import ssl
import openpyxl
import MySQLdb
import time

# 修改系统默认编码为utf-8
reload(sys)
sys.setdefaultencoding("utf-8")
ssl._create_default_https_context = ssl._create_unverified_context

# 创建全局列表存储数据，存放电影名字和链接地址
nameLists = []
linkLists = []


# 搜索豆瓣top100电影，保存成文件、excel、数据库
class TopMove:
    def __init__(self):
        self.URL = 'https://movie.douban.com/top250?start='

    def gethtml(self, page):
        try:
            url = self.URL + str(page * 25)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            html = response.read().decode('utf-8')
            return html
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u'链接豆瓣电影失败，错误原因：', e.reason
            return None

    @staticmethod
    def getlist(self):
        for page in range(10):
            print "正在获取电影列表" + str(page+1)
            html = self.gethtml(page)
            # 因为title的电影名有些存在两个title标签, 所以就在img中去正则匹配
            name = re.compile('<img alt="(.*?)".*?>', re.S)
            link = re.compile('<div class="hd">.*?<a.*?href="(.*?)".*?>.*?</a>', re.S)
            nameList = re.findall(name, html)
            linkList = re.findall(link, html)
            for name in nameList:
                if name.find('/') == -1:
                    nameLists.append(name)
                    for link in linkList:
                        linkLists.append(link)
        print "获取完毕"
        return nameLists, linkLists

    @staticmethod
    def save_text():
        try:
            f = open('date.txt', 'a')
            for i in range(250):
                f.write(nameLists[i])
                f.write('\t'*3)
                f.write(linkLists[i])
                f.write('\n')
            f.close()
        except Exception as e:
            print e
        print u"文件存储结束"

    @staticmethod
    def save_excel():
        try:
            wb = openpyxl.Workbook()
            sheet = wb.get_active_sheet()
            sheet.title = 'Move Top 250'
            for i in range(1, 251):
                one = 'a' + str(i)
                two = 'b' + str(i)
                sheet[one] = nameLists[i-1]
                sheet[two] = linkLists[i-1]
            wb.save(ur'豆瓣电影TOP250.xlsx')
        except Exception as e:
            print e
        print 'Excel 文件存储结束'

    @staticmethod
    def save_mysql():
        try:
            conn = MySQLdb.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='1234',
                db='db_admin',
                charset='utf8'
            )
            cursor = conn.cursor()
            print 'Connecting to MYSQL Success'
            cursor.execute('Drop table if EXISTS MovieTop')
            time.sleep(3)
            cursor.execute(
                """create table if not EXISTS MovieTop(
                    id int(4) not null primary key auto_increment,
                    movieName varchar(200),link varchar(200));""")
            for i in range(250):
                sql = 'insert into MovieTop(movieName,link) VALUES (%s,%s)'
                param = (nameLists[i], linkLists[i])
                cursor.execute(sql, param)
                conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print e
        print "Data Success Save in MYSQL"

    def start(self):
        self.getlist(self)
        self.save_text()
        self.save_excel()
        self.save_mysql()

dytop = TopMove()
dytop.start()
