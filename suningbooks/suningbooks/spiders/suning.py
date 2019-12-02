# -*- coding: utf-8 -*-
import re

import scrapy
from copy import deepcopy

from suningbooks.items import SuningbooksItem


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        dl_list = response.xpath('//div[@class="menu-item"]/dl')
        for dl in dl_list:
            item = SuningbooksItem()
            item['b_cate'] = dl.xpath('./dt/h3/a/text()').get()
            dd_list = dl.xpath('./dd/a')
            for dd in dd_list:
                item['m_cate'] = dd.xpath('./text()').get()
                item['m_url'] = dd.xpath('./@href').get()
                if item['m_url'] is not None:
                    yield scrapy.Request(
                        url=item['m_url'], callback=self.parse_books_list,
                        meta={"item": deepcopy(item)}
                    )

    def parse_books_list(self, response):
        item =deepcopy(response.meta["item"])
        book_list = response.xpath('//ul[@class="clearfix"]/li')
        for book in book_list:
            book_url = book.xpath('.//div[@class="res-info"]/p[@class="sell-point"]/a/@href').get()
            item['book_url'] = response.urljoin(book_url)
            item['book_comment']= response.xpath('.//div[@class="res-info"]/p[@class="com-cnt"]/a[1]/text()').get()
            yield scrapy.Request(url=item['book_url'], callback=self.parse_books,
                                 meta={"item": deepcopy(item)})

        page_count = int(re.findall(r'param.pageNumbers = "(.*?)";', response.body.decode())[0])
        current_page = int(re.findall(r'param.currentPage = "(.*?)";', response.body.decode())[0])
        page_id = re.findall(r"'cateid':'(.*?)'", response.body.decode())[0]
        if current_page < page_count:
            next_url = 'https://list.suning.com/emall/showProductList.do?ci={}&pg=03&cp={}&il=0&' \
                       'iy=-1&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAABC&id=IDENTIFYING&cc=870'.format(page_id, current_page+1)
            yield scrapy.Request(url=next_url, callback=self.parse_books_list,
                                 meta={"item": response.meta["item"]})

    def parse_books(self, response):
        item = response.meta['item']
        book_img_url = response.xpath('//div[@class="imgzoom-main"]/a/img/@src').get()
        item['book_img_url'] = response.urljoin(book_img_url)
        item['book_price'] = re.findall(r'"itemPrice":"(.*?)",' ,response.body.decode())
        item['book_price'] = item['book_price'][0] if len(item['book_price']) > 0 else None
        item['book_price'] = '¥' +  item['book_price']
        item['book_name'] = response.xpath('//div[@class="proinfo-title"]/h1/text()').getall()
        item['book_name'] = "".join([i.strip() for i in item['book_name'] if len(i.strip()) > 0])
        item['book_author'] = response.xpath('//ul[@class="bk-publish clearfix"]/li[1]/text()').getall()
        item['book_author'] ="".join([i.strip() for i in item['book_author'] if len(i.strip()) > 0])
        item['book_press'] = response.xpath('//ul[@class="bk-publish clearfix"]/li[2]/text()').get()
        if item['book_press'] is not None:
            item['book_press'] = "".join([i.strip() for i in item['book_press'] ])
        item['book_publish_data'] = response.xpath('//ul[@class="bk-publish clearfix"]/li[3]/span[2]/text()').get()
        yield item