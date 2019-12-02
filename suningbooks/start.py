from scrapy import cmdline


cmdline.execute(['scrapy', 'crawl', 'suning'])
# 等同于:cmdline.execute("scrapy crawl tupian".split())
