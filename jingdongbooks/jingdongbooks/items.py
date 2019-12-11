# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongbooksItem(scrapy.Item):
    book_name = scrapy.Field()
    book_author = scrapy.Field()
    book_press = scrapy.Field()
    book_publish_data = scrapy.Field()
    book_url = scrapy.Field()
    book_img_url = scrapy.Field()
    book_introduce = scrapy.Field()
    book_price = scrapy.Field()