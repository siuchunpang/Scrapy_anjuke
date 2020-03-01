# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjukespiderItem(scrapy.Item):
    # scene数据库字段
    scene_unique_name = scrapy.Field()
    scene_name = scrapy.Field()
    web_site = scrapy.Field()
    link_3d = scrapy.Field()
    data = scrapy.Field()

    shoot_count = scrapy.Field()
    creat_time = scrapy.Field()

    # scene_img数据库字段
    # FilesPipeline必须字段
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_paths = scrapy.Field()

    hotspots = scrapy.Field()
    results = scrapy.Field()
