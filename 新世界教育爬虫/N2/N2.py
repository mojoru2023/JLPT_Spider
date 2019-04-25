import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException

def call_page(url):
    req= requests.get(url)
      #  requests 中文编码的终极办法！
    if req.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding

        # encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
        global encode_content
        encode_content = req.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；
        return  encode_content



# 正则和lxml混用
def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    title = selector.xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/a/text()")
    links = selector.xpath('/html/body/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/a/@href')

    for i1,i2 in zip(title,links):
        big_list.append((i1,i2))

    return big_list








def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JLPT',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into XIJJY_n2 (title,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass

if __name__=="__main__":
    for num in range(1,78):
        print(num)
        url = "https://jp.xsjedu.org/list/N2/" + str(num) +"/"
        html = call_page(url)
        content = parse_html(html)
        insertDB(content)






# #
# create table XIJJY_n2(
# id int not null primary key auto_increment,
# title varchar(50),
# link varchar(50)
# ) engine=InnoDB  charset=utf8;


# drop table XIJJY_n2;