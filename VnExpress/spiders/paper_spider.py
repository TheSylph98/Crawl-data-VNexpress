import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import VnexpressItem


class PaperSpider(CrawlSpider):
    name = "paper"
    domain = 'https://vnexpress.net'
    start_urls = ['https://vnexpress.net/du-lich/p10']

    rules = (
        Rule(LinkExtractor(allow=r"du-lich/p[10-70]"),
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
        artilce['content'] = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "Normal", " " ))]').extract()
        items['content'] = ";".join(artilce['content'])

        artilce['author'] = response.xpath(
            '//strong/text()').extract()
        lenAuthor = len(artilce['author'])
        au = artilce['author']
        if lenAuthor == 0:
            items['author'] = 'unknow'
        elif lenAuthor > 1:
            items['author'] = au[lenAuthor-1]
        else:
            items['author'] = au[0]

        items['title'] = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "title-detail", " " ))]/text()').extract()[0]
        items['publish_date'] = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "date", " " ))]/text()').extract()[0]
        # items['author'] =
        items['description'] = response.xpath(
            '//p[@class="description"]').extract()[0]
        items['topic'] = response.xpath(
            '//ul[@class="breadcrumb"]//li//h2//a/@title').extract()[0]

        yield items
