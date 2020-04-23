import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import VnexpressItem


class PaperSpider(CrawlSpider):
    name = "paper"
    domain = 'https://vnexpress.net'
    start_urls = ['https://vnexpress.net/thoi-su-p2']

    rules = (
        Rule(LinkExtractor(allow=r"thoi-su-p[2-50]"),
             callback="get_links", follow=True),
    )

    def get_links(self, response):
        urls = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "description", " " ))]/a/@href').extract()
        print("--------------")
        print(urls)
        print("--------------")
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.parse_item)

    def parse_item(self, response):
        # .encode('utf-8').strip()
        items = VnexpressItem()
        artilce = {}
        artilce['title'] = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "title-detail", " " ))]/text()').extract()[0]
        artilce['publish_date'] = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "date", " " ))]/text()').extract()[0]
        artilce['content'] = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "Normal", " " ))]').extract()

        items['title'] = artilce['title']
        items['content'] = ",".join(artilce['content']).strip()
        items['publish_date'] = artilce['publish_date']

        yield items
