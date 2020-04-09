# -*- coding: utf-8 -*-
import scrapy

from duanziwang.items import DuanziwangItem


class DuanziSpider(scrapy.Spider):
    name = 'duanzi'
    allowed_domains = ['duanziwang.com']
    start_urls = ['http://duanziwang.com/category/%E7%BB%8F%E5%85%B8%E6%AE%B5%E5%AD%90/1/']

    def parse(self, response):
        contents = response.css('main article')
        for duanzi in contents:
            item = DuanziwangItem()
            title = duanzi.css('.post-title a::text').extract_first()
            time = duanzi.css('.post-meta time::text').extract()
            release_time = time[0]
            heat = time[1]
            like = duanzi.css('.post-meta time span::text').extract_first()
            content = duanzi.css('.post-content p::text').extract()
            for field in item.fields.keys():
                item[field] = eval(field)
            if item['content'] == []:
                item['content'] = item['title']
            else:
                yield item
        next_page = response.css('.pagination .next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)  # 拼接URL urljoin(start_urls, next_page)
            yield scrapy.Request(next_page, callback=self.parse)