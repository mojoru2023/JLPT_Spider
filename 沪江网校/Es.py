# ! -*- coding:utf-8 -*-

import time
import re
import pymysql
import requests
from selenium import webdriver
# 还是要用PhantomJS
import datetime
import string
from lxml import etree




def call_pages(url):
    driver = webdriver.Chrome()
    driver.get(url)
    # time.sleep(1)
    html = driver.page_source
    driver.close()
    return html

def enumerate_fn_odd(lit):    # 要取到索引值为奇数的部分！
    '''enumerate函数：获取每个元素的索引和值
     可以返回索引和值  even number 是偶数 odd number 是奇数'''
    '''甚至可以做一个装饰器！'''
    odd_con = []
    for index, value in enumerate(lit):
        if index % 2  == 0:  # 记住索引是从０开始的！
            odd_con.append(value)
        else:
            pass
    return  odd_con


def parse_pages(html):


    big_list = []
    selector = etree.HTML(html)
    title = selector.xpath('/html/body/div[5]/div/div[1]/div[1]/ul//a[2]/span/text()')
    link = selector.xpath('/html/body/div[5]/div/div[1]/div[1]/ul//a[2]/@href')
    link_odd = enumerate_fn_odd(link)
    link_f  = []
    for item in link_odd:
        link_f.append('https://jp.hjenglish.com'+item)


    for i1,i2 in zip(title, link_f):
        big_list.append((i1,i2))

    return big_list



def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JLPT',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # 这里是判断big_list的长度，不是content字符的长度
    try:
        cursor.executemany('insert into Es (title,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except Exception :
        print('出列啦')







if __name__ == '__main__':
    for num in range(27,47):
        url = 'https://jp.hjenglish.com/new/N1N2/page'  + str(num)  + '/'
        html = call_pages(url)
        content = parse_pages(html)
        insertDB(content)









# create table Es (
# id int not null primary key auto_increment,
# title varchar(100),
# link varchar(150)
# ) engine =InnoDB charset=utf8;
#
# drop table down_links;
#
#
# drop table down_links;
# select count(*) from down_links;
#





