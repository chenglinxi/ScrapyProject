# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningbooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    b_cate = scrapy.Field()
    m_cate = scrapy.Field()
    m_url = scrapy.Field()
    book_url = scrapy.Field()
    book_price = scrapy.Field()
    book_comment = scrapy.Field()
    book_img_url = scrapy.Field()
    book_name = scrapy.Field()
    book_author = scrapy.Field()
    book_press = scrapy.Field()
    book_publish_data = scrapy.Field()
