# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql


class MongoPipeline(object):

    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

class MysqlPipeline(object):
    def __init__(self):
        # 连接MySQL数据库
        self.connect = pymysql.connect(host='localhost', user='root', password='123456', port=3306)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:

            self.cursor.execute('create database scrapy')
            print('创建数据库成功Daatabase created')
        except:
            print('Database scrapy exists!')
        self.connect.select_db('scrapy')
        try:
            self.cursor.execute('create table dangdang(id int AUTO_INCREMENT PRIMARY KEY, 一类 VARCHAR(10) NULL, '
                                '二类 VARCHAR(10) NULL, 三类 VARCHAR(20) NULL, 类别URL VARCHAR(100) NULL,'
                                '图书图片 VARCHAR(100) NULL, 图书名 VARCHAR(100) NULL, 图书URL VARCHAR(100) NULL,'
                                '图书简介 VARCHAR(200) NULL, 价格 VARCHAR(20) NULL, 作者 VARCHAR(100) NULL,'
                                '出版时间 VARCHAR(10) NULL, 出版社 VARCHAR(20) NULL, 评论 VARCHAR(10)  NULL)')
            print('创建数据表成功Tables created')
        except:
            print('The table dangdang exists!')
        # 往数据库里面写入数据
        self.cursor.execute(
            'insert into dangdang(一类, 二类, 三类, 类别URL, 图书图片, 图书名, 图书URL, 图书简介, 价格, 作者, 出版时间, 出版社, 评论)VALUES ("{}","{}","{}","{}","{}","{}","{}","{}",'
            '"{}","{}","{}","{}","{}")'.format(item['b_cate'], item['m_cate'], item['s_cate'], item['s_href'], item['book_img'], item['book_name'], item['book_url'],
                                               item['book_desc'], item['book_price'], item['book_author'], item['book_publish_data'], item['book_press'], item['book_comment']))
        self.connect.commit()
        return item

    # 关闭数据库
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
