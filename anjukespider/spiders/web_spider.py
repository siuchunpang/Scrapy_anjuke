import time
import scrapy
import datetime
import re

from selenium import webdriver
from anjukespider.items import AnjukespiderItem


class WebsiteSpider(scrapy.Spider):
    spider_count = 1
    name = 'anjukespider'

    start_urls = ['https://beijing.anjuke.com/sale/v3/']

    def validate_title(self, title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title

    def parse(self, response):
        print("第%d次爬虫" % self.spider_count)
        link_list = response.css("a.houseListTitle")
        if link_list:
            print("开始解析网站...")
            for link in link_list:
                item = AnjukespiderItem()
                scene_name = self.validate_title(link.css("::attr(title)").get())
                item["scene_name"] = scene_name
                item["web_site"] = link.css("::attr(href)").get()
                item["creat_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield item
            # next_page = response.css('a.aNxt::attr(href)').get()
            # if next_page is not None:
            #     self.spider_count += 1
            #     next_page = response.urljoin(next_page)
            #     yield scrapy.Request(next_page, callback=self.parse)

            print("解析网站完成！")
            print("爬虫次数：", self.spider_count)
        else:
            self.spider_error()

    def spider_error(self):
        print("防爬机制已阻拦，需要人工操作")
        driver = webdriver.Chrome()
        driver.get("https://beijing.anjuke.com/sale/v3/")
        driver.maximize_window()
        time.sleep(8)
        return self.spider_count
