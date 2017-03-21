# -*- coding:utf-8 -*-

# codes.BOM_UTF8可以防止写excel时出现中文乱码问题
import codecs
import sys

import requests
import csv
import random
import time
import socket
from bs4 import BeautifulSoup

# 引入这个解决Python的str默认是ascii编码，和unicode编码冲突
reload(sys)
sys.setdefaultencoding('utf-8')


def get_content(url):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    timeout = random.choice(range(80, 180))
    rep = ""
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print "Strange error %s" % e
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print "Strange error creating socket: %s" % e
            time.sleep(random.choice(range(20, 60)))

    return rep.text


def get_data(html_text):
    final = []
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    # 获取body部分，找到id为7d的div，获取ul下的所有li，即7天的天气元素
    body = bs.body
    data = body.find('div', {'id': '7d'})
    ul = data.find('ul')
    li = ul.find_all('li')

    for day in li:
        temp = []
        # 找到日期，天气状况
        date = day.find('h1').string
        temp.append(date)
        inf = day.find_all('p')
        temp.append(inf[0].string,)
        # 天气预报可能没有当天的最高气温（到了傍晚，就是这样），需要加个判断语句,来输出最低气温
        if inf[1].find('span') is None:
            temperature_highest = None
        else:
            temperature_highest = inf[1].find('span').string
            temperature_highest = temperature_highest.replace('℃', '')
        temperature_lowest = inf[1].find('i').string
        temperature_lowest = temperature_lowest.replace('℃', '')
        temp.append(temperature_highest)
        temp.append(temperature_lowest)
        final.append(temp)

    return final


def write_data(data, name):
    file_name = name
    with open(file_name, 'wb') as f:
        f.write(codecs.BOM_UTF8)
        f_csv = csv.writer(f, dialect='excel')
        f_csv.writerows(data)


if __name__ == '__main__':
    url_addr = 'http://www.weather.com.cn/weather/101230101.shtml'
    html = get_content(url_addr)
    result = get_data(html)
    write_data(result, 'weather.csv')
