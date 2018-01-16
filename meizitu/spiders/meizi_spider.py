import scrapy
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader, Identity
from meizitu.items import MeizituItem


class MeiziSpider(scrapy.Spider):
    name = 'meizi'
    allowed_domains = ["jandan.net"]
    start_urls = [
        'http://jandan.net/ooxx'
    ]

    def parse(self, response):
        sel = Selector(response)
        for link in sel.xpath('//div[@class="text"]/p/img/@src').extract():
            request = scrapy.Request(link, callback=self.parse_item)
            yield request
        pages = sel.xpath('//div[@class="comments"]/div[@class="cp-pagenavi"/a/@href]').extract()
        print 'pages: %s' % pages
        if len(pages) > 2:
            page_link = pages[-2]
            request = scrapy.Request('%s' % page_link, callback=self.parse)
            yield request

    def parse_item(self, response):
        l = ItemLoader(item=MeizituItem(), response=response)
        # l.add_xpath('name', '//div[@class="postContent"]/div[@id="picture"]/p/a/text()')
        # l.add_xpath('tags', '//div[@class="postContent"]')
        l.add_xpath('img_url', '//div[@class="text"]/p/br/img/@src', Identity())
        l.add_value('url', response.url)

        return l.load_item()
