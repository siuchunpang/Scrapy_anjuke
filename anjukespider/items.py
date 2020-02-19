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
    creat_time = scrapy.Field()
    link_3d = scrapy.Field()

    # hotspots = scrapy.Field()

    # img_count = scrapy.Field()
    # hotspots_index = scrapy.Field()
    # img_index = scrapy.Field()
    # img_urls = scrapy.Field()


# class ImageItem(scrapy.Item):
#     # 存放url的下载地址
#     image_urls = scrapy.Field()
#     # 图片下载路径、url和校验码等信息（图片全部下载完成后将信息保存在images中）
#     images = scrapy.Field()
#     # 图片的本地保存地址
#     image_paths = scrapy.Field()
#
#     img_count = scrapy.Field()
#     hotspots_index = scrapy.Field()
#     img_index = scrapy.Field()
#     img_url = scrapy.Field()


class FileItem(scrapy.Item):
    file_json = scrapy.Field()
    file_name = scrapy.Field()
    # 存放url的下载地址
    file_urls = scrapy.Field()
    # 图片下载路径、url和校验码等信息（图片全部下载完成后将信息保存在images中）
    files = scrapy.Field()
    # 图片的本地保存地址
    file_paths = scrapy.Field()

    file_count = scrapy.Field()
    hotspots_index = scrapy.Field()
    file_index = scrapy.Field()
    file_url = scrapy.Field()
