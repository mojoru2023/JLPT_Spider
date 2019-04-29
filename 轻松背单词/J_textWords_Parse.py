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

from s_links import f_list

driver = webdriver.Chrome()
#　因为只做一次，所以尽可能要全面！

def call_pages(url):
    driver.get(url)
    time.sleep(1)
    html = driver.page_source

    return html


def parse_pages(html):
    big_list = []
    selector = etree.HTML(html)
    J_word1 = selector.xpath('/html/body/div[5]/div[2]/table/tbody/tr/td[3]/div/span/text()')
    J_word2 = selector.xpath('/html/body/div[5]/div[2]/table/tbody/tr/td[4]/div/span/text()')
    A_word = selector.xpath('/html/body/div[5]/div[2]/table/tbody/tr/td[6]/div/span/text()')
    type = selector.xpath('/html/body/div[5]/div[2]/table/tbody/tr/td[7]/text()')
    type_f = type[1:]



    for i1,i2,i3,i4 in zip(J_word1, J_word2,A_word,type_f):
        big_list.append((i1,i2,i3,i4))

    return big_list



def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JLPT',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # 这里是判断big_list的长度，不是content字符的长度
    try:
        cursor.executemany('insert into ALlText_words_Parse (J_word1,J_word2,A_word,type_f) values (%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except Exception :
        print('出列啦')







if __name__ == '__main__':
    for url in f_list:

        html = call_pages(url)
        content = parse_pages(html)
        insertDB(content)
        print(url)










# create table ALlText_words_Parse (
# id int not null primary key auto_increment,
# J_word1 varchar(80),
# J_word2 varchar(80),
# A_word varchar(80),
# type_f varchar(20)
# ) engine =InnoDB charset=utf8;
# # #
# drop table ALlText_words_Parse;
#


#





