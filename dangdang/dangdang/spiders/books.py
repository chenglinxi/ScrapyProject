# -*- coding: utf-8 -*-
import re

import scrapy
from copy import deepcopy


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://book.dangdang.com/']

    def parse(self, response):
        # 大分类分组
        div_list = response.xpath('//div[@class="con flq_body"]/div')
        for div in div_list:
            item = {}
            b_cate1 = div.xpath('./dl/dt/a/text()').getall()
            b_cate1 = [i.strip() for i in b_cate1 if len(i.strip()) > 0]
            b_cate2 = div.xpath('./dl/dt/text()').getall()
            b_cate2 = [i.strip() for i in b_cate2 if len(i.strip()) > 0]
            item["b_cate"] = b_cate1 +b_cate2
            item["b_cate"] ="".join([i for i in item["b_cate"] if len(i) != 0]) # 去除空元素
            item["b_cate"] = re.sub(r'\s|－|/', '', item["b_cate"])
            # 中间分类分组
            dl_list = div.xpath('./div//dl[@class="inner_dl"]')
            for dl in dl_list:
                item["m_cate"] = dl.xpath('./dt//text()').getall()
                item["m_cate"] = [i.strip() for i in item["m_cate"] if len(i.strip()) > 0][0]
                # 小分类分'组
                dd_list = dl.xpath('./dd/a')
                for dd in dd_list:
                    item["s_href"] = dd.xpath('./@href').get()
                    item["s_cate"] = dd.xpath('./text()').get()
                    if item["s_href"] is not None:
                        yield scrapy.Request(
                            url=item["s_href"], callback=self.parse_book,
                            meta= {"item": deepcopy(item)}
                        )

    def parse_book(self, response):
        item = response.meta["item"]
        li_list = response.xpath('//ul[@class="bigimg"]/li')
        for li in li_list:
            item["book_img"] = li.xpath('./a[@class="pic"]/img/@src').get()
            if item["book_img"] == 'images/model/guan/url_none.png':
                item["book_img"] = li.xpath('./a[@class="pic"]/img/@data-original').get()
            item["book_name"] = li.xpath('./p[@class="name"]/a/text()').get()
            item["book_url"] = li.xpath('./p[@class="name"]/a/@href').get()
            item["book_desc"] = li.xpath('./p[@class="detail"]/text()').get()
            item["book_price"] = li.xpath('./p[@class="price"]/span[@class="search_now_price"]/text()').get()
            item["book_author"] ="".join(li.xpath('./p[@class="search_book_author"]/span[1]/a/text()').getall())
            item["book_publish_data"] = li.xpath('./p[@class="search_book_author"]/span[2]/text()').get()
            item["book_publish_data"] = re.sub(r'\s|－|/', '', str(item["book_publish_data"]))
            item["book_press"] = li.xpath('./p[@class="search_book_author"]/span[3]/a/text()').get()
            item["book_comment"] = li.xpath('./p[@class="search_star_line"]/a/text()').get()
            yield item
        next_page = response.xpath('//div[@class="paging"]//li[@class="next"]/a/@href').get()
        if next_page:
            next_page = response.urljoin(next_page) #拼接URL
            print(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse_book,
                                 meta= {"item": item})



