# -*- coding: utf-8 -*-

import requests
from lxml import etree
import re

def getUrl():
    baseUrl = 'https://www.gushiwen.org/'
    urls = []
    for i in range(2):
        url = baseUrl + "default_" + str(i) + ".aspx"
        urls.append(url)
    return urls

def getData(url):
    html = requests.get(url)
    html = etree.HTML(html.text)
    poetry_title = html.xpath('.//div[@class="sons"]/div[@class="cont"]//b/text()')
    poetry_author = html.xpath('.//div[@class="sons"]/div[@class="cont"]/p[@class="source"]//a/text()')
    poetry_contents = html.xpath('//div[@class="contson"]')
    for index, content in enumerate(poetry_contents):
        title = poetry_title[index]
        author_dynasty = poetry_author[index * 2]
        author_name = poetry_author[index * 2 + 1]
        author = author_dynasty + "-" + author_name
        # 获取这个html对象
        content = etree.tostring(content, encoding='utf-8').decode('utf-8')
        # 将标签符号全部替换掉
        content = re.sub(r'<.*?>|\n|', '', content)
        # 将首尾的空格也去掉
        content = re.sub(r'\u3000\u3000', '', content)
        print title
        print author
        print content
        print ""


if __name__ == '__main__':
    urls = getUrl()
    for url in urls:
        getData(url)
