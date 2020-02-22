import json
import scrapy
import datetime
import re
from anjukespider.items import AnjukespiderItem
from anjukespider.items import FileItem


class WebsiteSpider(scrapy.Spider):
    spider_count = 1
    name = 'anjukespider'

    start_urls = ['https://beijing.anjuke.com/sale/v3/']
    # start_urls = ["http://httpbin.org/get"]

    def validate_title(self, title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title

    def parse(self, response):
        try:
            print("第%d次爬虫" % self.spider_count)
            link_list = response.css("a.houseListTitle")
            print("开始解析网站...")
            for link in link_list:
                anjuke_item = AnjukespiderItem()
                scene_name = self.validate_title(link.css("::attr(title)").get())
                # item["img_count"] = 0
                anjuke_item["scene_name"] = scene_name
                anjuke_item["web_site"] = link.css("::attr(href)").get()
                anjuke_item["creat_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield scrapy.Request(anjuke_item['web_site'], meta={'anjuke_item': anjuke_item}, callback=self.parse_3d)
                # break

            print("解析网站完成！")
            print("爬虫次数：", self.spider_count)
            self.spider_count += 1

            next_page = response.css('a.aNxt::attr(href)').get()
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parse)
        except Exception as e:
            print("parse_error：", e)

    def parse_3d(self, response):
        try:
            link_3d = response.xpath('//*[@id="qj_pic_wrap"]/div/iframe/@src').get()
            anjuke_item = response.meta['anjuke_item']
            if link_3d is not None:
                # item["img_count"] += 1
                anjuke_item["link_3d"] = link_3d
                yield anjuke_item
                yield scrapy.Request(link_3d, meta={'anjuke_item': anjuke_item}, callback=self.parse_img)
            else:
                print("该房间没有3D场景")
                anjuke_item["link_3d"] = ""
                yield anjuke_item
        except Exception as e:
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
                hotspots = data['HotSpots']

                for hotspots_index, hotspot in enumerate(hotspots):
                    file_item = FileItem()
                    file_item["file_name"] = anjuke_item["scene_name"]
                    file_item["file_json"] = data
                    file_urls = hotspot['TileImagesPath']
                    file_item["hotspots_index"] = hotspots_index
                    file_item["file_urls"] = file_urls
                    yield file_item

            # print("解析图片完成！")
            # shoot_count = len(hotspots)
            # yield shoot_count
        except Exception as e:
            print("parse_img_error：", e)

