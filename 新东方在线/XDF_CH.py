# -*- coding:utf-8 -*-
import datetime
import re
import time
import requests

import pymysql

from lxml import etree

from selenium import webdriver


def get_one_page(url):

    driver.get(url)
    html = driver.page_source
    return html




def parse_note(html):
    big_list = []
    selector = etree.HTML(html)
    title = selector.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/ul/li/h3/a/text()')
    links = selector.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/ul/li/h3/a/@href')

    for i1,i2 in zip(title,links):
        big_list.append((i1,i2))
    return big_list


def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='XDF',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into CH (title,links) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass


if __name__ == '__main__':
    driver = webdriver.Chrome()
    url = 'http://language.koolearn.com/jp/cihui/'

    # for num in range(1,426):
    # url = 'http://language.koolearn.com/jp/cihui/' + str(num)+ '.html'
    html = get_one_page(url)
    content = parse_note(html)
    insertDB(content)
    print(url)




# create table CH (
# id int not null primary key auto_increment,
# title text,
# linkS text
# ) engine =InnoDB charset=utf8;

# drop table CH;

