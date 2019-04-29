#! -# ! -*- coding:utf-8 -*-

import time
import re
import pymysql
import requests
from selenium import webdriver
# 还是要用PhantomJS
import datetime
import string
from lxml import etree

driver = webdriver.Chrome()


def call_pages(url):
    driver.get(url)
    time.sleep(3)
    html = driver.page_source

    return html


def parse_pages(html):
    big_list = []
    selector = etree.HTML(html)
    title = selector.xpath('/html/body/div[5]/div[2]/table/tbody/tr/td[1]/strong/text()')
    links = selector.xpath('/html/body/div[5]/div[2]/table/tbody/tr/td[2]/a[1]/@href')
    title_f = title[1:]
    for i1,i2 in zip(title_f, links):
        big_list.append((i1,'http://jp.qsbdc.com/jpword/'+i2))

    return big_list



def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JLPT',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # 这里是判断big_list的长度，不是content字符的长度
    try:
        cursor.executemany('insert into ALlText_words_link1 (title,links) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except Exception :
        print('出列啦')







if __name__ == '__main__':
    lf = ['http://jp.qsbdc.com/jpword/lesson_list.php?book_id=9',
          'http://jp.qsbdc.com/jpword/lesson_list.php?book_id=1',
          'http://jp.qsbdc.com/jpword/lesson_list.php?book_id=2',
          'http://jp.qsbdc.com/jpword/lesson_list.php?book_id=3',
          'http://jp.qsbdc.com/jpword/lesson_list.php?book_id=4',
          'http://jp.qsbdc.com/jpword/lesson_list.php?book_id=5',
          'http://jp.qsbdc.com/jpword/lesson_list.php?book_id=6',
          'http://jp.qsbdc.com/jpword/lesson_list.php?book_id=7',
          'http://jp.qsbdc.com/jpword/lesson_list.php?book_id=8']
    for url in lf:


        html = call_pages(url)
        content = parse_pages(html)
        insertDB(content)
        print(url)










# create table ALlText_words_link1 (
# id int not null primary key auto_increment,
# title text,
# links text
# ) engine =InnoDB charset=utf8;

# drop table ALlText_words_link1;
#





