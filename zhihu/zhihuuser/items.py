# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# import scrapy
#
#
# class UserItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     id = scrapy.Field()

from scrapy import Item, Field


class UserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    name = Field()
    follower_count = Field()
    headline = Field()
    url = Field()
    url_token = Field()
    answer_count = Field()
    avatar_url = Field()
    articles_count = Field()
