# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from jingdongbooks.items import JingdongbooksItem


class JingdongSpider(CrawlSpider):
    name = 'jingdong'
    allowed_domains = ['jd.com']
    start_urls = ['https://list.jd.com/list.html?cat=1713,3258&page=1&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main']

    rules = (
        Rule(LinkExtractor(allow=r'.*,\d+\&page=\d+\.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        li_list = response.xpath('//div[@id="plist"]/ul[@class="gl-warp clearfix"]/li')
        for li in li_list:
            item = {}
            item['book_name'] = li.xpath('./div/div[@class="p-name"]/a/em/text()').get()
            item['book_name'] = item['book_name'].strip()
            item['book_author'] = li.xpath('./div/div[@class="p-bookdetails"]/span[@class="p-bi-name"]/span/a/text()').get()
            if item['book_author'] is not None:
                item['book_author'] = item['book_author'].strip()
            item['book_press'] = li.xpath('./div/div[@class="p-bookdetails"]/span[@class="p-bi-store"]/a/text()').get()
            item['book_publish_data'] = li.xpath('./div/div[@class="p-bookdetails"]/span[@class="p-bi-date"]/text()').get()
            item['book_publish_data'] = item['book_publish_data'].strip()
            book_url = li.xpath('./div/div[@class="p-img"]/a/@href').get()
            item['book_url'] = response.urljoin(book_url)
            img_url = li.xpath('./div/div[@class="p-img"]/a/img/@src').get()
            if img_url is not None:
                item['book_img_url']= 'https:' + img_url
            yield scrapy.Request(url=item['book_url'], callback=self.parse_book,
                                 meta={"item": item})
        # next_page = response.xpath('//div[@class="page clearfix"]//a[@class="pn-next"]/@href').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     print(next_page)
        #     yield scrapy.Request(url=next_page, callback=self.parse_item)


    def parse_book(self, response):
        item = response.meta["item"]
        item['book_introduce'] = response.xpath('//div[class="book-detail-content"]/p//text()').getall()
        item['book_price'] = response.xpath('//strong[@class="p-price"]//text()').getall()
        print(item)