# -*- coding: utf-8 -*-
import scrapy

from itcast.items import ItcastItem


class ItcastsSpider(scrapy.Spider):
    name = 'itcasts'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml#ajavaee/']

    def parse(self, response):
        teachers = response.css('.tea_txt ul li')
        for teacher in teachers:
            item = ItcastItem()
            name = teacher.css('.li_txt h3::text').extract_first()
            title = teacher.css('.li_txt h4::text').extract_first()
            introduction = teacher.css('.li_txt p::text').extract_first()
            item['name'] = name
            item['title'] = title
            item['introduction'] = introduction
            yield item

        # next = response.css('.pager .next a::attr(href)').extract_first()
        # url = response.urljoin(next)
        # yield scrapy.Request(url=url, callback=self.parse)
