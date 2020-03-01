import json
import scrapy
import datetime
import re
import logging
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
        try:
            # logging.info("第%d次爬虫" % self.spider_count)
            print("爬取第%d页" % self.spider_count)
            link_list = response.css("a.houseListTitle")
            # logging.info("开始解析网站...")
            for link in link_list:
                anjuke_item = AnjukespiderItem()
                scene_name = self.validate_title(link.css("::attr(title)").get())
                href = link.css("::attr(href)").get()
                scene_unique_name = href.split("?")[0]
                anjuke_item["scene_unique_name"] = scene_unique_name[-11:]
                anjuke_item["scene_name"] = scene_name
                anjuke_item["web_site"] = href
                anjuke_item["creat_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("开始解析%s场景..." % scene_unique_name[-11:])
                yield scrapy.Request(anjuke_item['web_site'], meta={'anjuke_item': anjuke_item}, callback=self.parse_3d)
                # break

            next_page = response.css('a.aNxt::attr(href)').get()
            if next_page is not None and self.spider_count < 5:
                self.spider_count += 1
                yield scrapy.Request(next_page, callback=self.parse)
            else:
                print("共爬取%d页" % self.spider_count)
        except Exception as e:
            # logging.error("parse_error：", e)
            print("parse_error：", e)

    def parse_3d(self, response):
        try:
            link_3d = response.xpath('//*[@id="qj_pic_wrap"]/div/iframe/@src').get()
            anjuke_item = response.meta['anjuke_item']
            if link_3d is not None:
                anjuke_item["link_3d"] = link_3d
                yield scrapy.Request(link_3d, meta={'anjuke_item': anjuke_item}, callback=self.parse_img)
            else:
                # logging.warning("该房间没有3D场景")
                print("该房间没有3D场景")
                anjuke_item["link_3d"] = ""
                yield anjuke_item
        except Exception as e:
            # logging.error("parse_3d_error：", e)
            print("parse_3d_error：", e)

    def parse_img(self, response):
        try:
            anjuke_item = response.meta['anjuke_item']
            data_3d_list = re.findall(r'VRHOUSE_DATA_3D = (.+?)    </script>', response.text)
            if not data_3d_list:
                data_3d_list = re.findall(r'\(\'vrdataload\',(.+?)\);', response.text)
            if data_3d_list is not []:
                data_3d = data_3d_list[0].replace("\\", "")
                data = json.loads(data_3d, strict=False)
                anjuke_item["data"] = data
                anjuke_item["hotspots"] = data['HotSpots']
                anjuke_item["shoot_count"] = len(anjuke_item["hotspots"])
                yield anjuke_item

        except Exception as e:
            # logging.error("parse_img_error：", e)
            print("parse_img_error：", e)

