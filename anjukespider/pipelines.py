import json
import os
import logging

from scrapy.pipelines.files import FilesPipeline
from anjukespider.model.scene import Scene, SceneImg
from anjukespider.model.config import DBSession
from anjukespider.model.config import Redis
from anjukespider.items import AnjukespiderItem
from anjukespider.items import FileItem
from anjukespider.settings import FILES_STORE
from scrapy.exceptions import DropItem
from scrapy import Request


# 数据去重
# class DuplicatesPipeline(object):
#     def process_item(self, item, spider):
#         if Redis.hexists("duplicate", item['scene_name']):
#             print("Duplicate item found: %s" % item)
#             raise DropItem("Duplicate item found: %s" % item)
#         else:
#             Redis.hset("duplicate", item['scene_name'], 1)
#             return item


# 下载图片（自带）
class ImgDownloadPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        file_url = request.url
        file_link_name = file_url[24:56]
        return '%s/hotspot_%s/%s.jpg' % (item["file_name"], item["hotspots_index"], file_link_name)

    def get_media_requests(self, item, info):
        if isinstance(item, FileItem):
            # logging.info("下载图片...")
            print("下载图片...")
            for file_url in item['file_urls']:
                yield Request(url=file_url, meta={'item': item})

    def item_completed(self, results, item, info):
        if isinstance(item, FileItem):
            file_paths = [x['path'] for ok, x in results if ok]
            # logging.info("file_paths：", file_paths)
            print("file_paths：", file_paths)
            if not file_paths:
                raise DropItem("Item contains no images")
            item['file_paths'] = file_paths
            print("hotspots_index：", item["hotspots_index"])
            return item
        else:
            return item


# 下载Json文件
class JsonDownloadPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, FileItem):
            scene_path = FILES_STORE + item["file_name"]
            if not os.path.exists(scene_path + "\\scene.json"):
                # logging.info("下载Json文件")
                print("下载Json文件")
                with open(scene_path + "\\scene.json", 'w') as file:
                    json.dump(item["file_json"], file)
        return item


# 数据库操作
class DBPipeline(object):
    def __init__(self):
        self.session = DBSession()

    def process_item(self, item, spider):
        try:
            # self.session.begin_nested()
            if isinstance(item, AnjukespiderItem):
                # logging.info("录入数据库")
                print("录入数据库scene")
                sql_scene = Scene(
                    scene_unique_name=item["scene_unique_name"],
                    scene_name=item["scene_name"],
                    web_site=item["web_site"],
                    link_3d=item["link_3d"],
                    shoot_count=item["shoot_count"],
                    creat_time=item["creat_time"]
                )
                self.session.add(sql_scene)
            elif isinstance(item, FileItem):
                # logging.info("录入数据库")
                print("录入数据库scene_img")
                for img_url in item['file_urls']:
                    sql_img = SceneImg(
                        scene_id=sql_scene.id,
                        img_url=img_url,
                    )
                    self.session.add(sql_img)
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            # logging.error("DBPipeline_error：", e)
            print("DBPipeline_error：", e)
        return item

    def close_spider(self, spider):
        self.session.close()
