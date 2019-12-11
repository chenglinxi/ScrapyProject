from scrapy import cmdline


cmdline.execute(['scrapy', 'crawl', 'books'])
# 等同于:cmdline.execute("scrapy crawl tupian".split())
