import json

from scrapy.pipelines.files import FilesPipeline
from anjukespider.model.scene import Scene
from anjukespider.model.config import DBSession
from anjukespider.model.config import Redis
from anjukespider.items import AnjukespiderItem
from anjukespider.items import FileItem
from scrapy.exceptions import DropItem
from scrapy import Request


# 数据去重
class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        if Redis.hexists("duplicate", item['scene_name']):
            print("Duplicate item found: %s" % item)
            raise DropItem("Duplicate item found: %s" % item)
        else:
            Redis.hset("duplicate", item['scene_name'], 1)
            return item


# 下载图片（自带）
class ImgDownloadPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        file_url = request.url
        file_link_name = file_url[24:56]
        return '%s/hotspot_%s/%s.jpg' % (item["file_name"], item["hotspots_index"], file_link_name)

    def get_media_requests(self, item, info):
        if isinstance(item, FileItem):
            for file_url in item['file_urls']:
                yield Request(url=file_url, meta={'item': item})

    def item_completed(self, results, item, info):
        if isinstance(item, FileItem):
            file_paths = [x['path'] for ok, x in results if ok]
            print("file_paths：", file_paths)
            if not file_paths:
                raise DropItem("Item contains no images")
            item['file_paths'] = file_paths
            return item
        else:
            return item


# 下载Json文件
class JsonDownloadPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, FileItem):
            with open("F:\\Project\\Scrapy_anjuke\\anjukespider\\scene\\%s\\scene.json" % item["file_name"], 'w') as file:
                json.dump(item["file_json"], file)
        return item


# 数据库操作
class DBPipeline(object):
    def __init__(self):
        self.session = DBSession()

    def process_item(self, item, spider):
        if isinstance(item, AnjukespiderItem):
            try:
                sql = Scene(
                    scene_name=item["scene_name"],
                    web_site=item["web_site"],
                    link_3d=item["link_3d"],
                    creat_time=item["creat_time"]
                )
                self.session.add(sql)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                print("DBPipeline_error：", e)
        else:
            return item

    def close_spider(self, spider):
        self.session.close()
