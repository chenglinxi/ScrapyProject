from scrapy import cmdline


cmdline.execute(['scrapy', 'crawl', 'jingdong'])
# 等同于:cmdline.execute("scrapy crawl tupian".split())
