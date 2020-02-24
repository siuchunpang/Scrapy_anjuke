# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjukespiderItem(scrapy.Item):
    # 数据库字段
    scene_name = scrapy.Field()
    web_site = scrapy.Field()
    link_3d = scrapy.Field()
    shoot_count = scrapy.Field()
    creat_time = scrapy.Field()


class FileItem(scrapy.Item):
    file_json = scrapy.Field()
    file_name = scrapy.Field()
    # 存放url的下载地址
    file_urls = scrapy.Field()
    # 图片下载路径、url和校验码等信息（图片全部下载完成后将信息保存在images中）
    files = scrapy.Field()
    # 图片的本地保存地址
    file_paths = scrapy.Field()

    hotspots_index = scrapy.Field()
