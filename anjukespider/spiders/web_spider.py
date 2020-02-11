import scrapy
import datetime
from anjukespider.items import AnjukespiderItem


class WebsiteSpider(scrapy.Spider):
    spider_count = 1
    name = 'anjukespider'

    start_urls = ['https://beijing.anjuke.com/sale/v3/']

    def parse(self, response):
        item = AnjukespiderItem()
        print("第%d次爬虫" % self.spider_count)
        for link_list in response.css("a.houseListTitle"):
            yield {
                item["scene_name"]: link_list.css("a.houseListTitle::attr(title)").get(),
                item["web_site"]: link_list.css("a.houseListTitle::attr(href)").get(),
                item["creat_time"]: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        # next_page = response.css('a.aNxt::attr(href)').get()
        # if next_page is not None:
        #     self.spider_count += 1
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)



