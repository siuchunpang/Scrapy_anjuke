from anjukespider.model.scene import Scene
from anjukespider.model.config import DBSession
from anjukespider.model.config import Redis
from scrapy.exceptions import DropItem


# 数据去重
class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        if Redis.hexists("duplicate", item['scene_name']):
            print("Duplicate item found: %s" % item)
            raise DropItem("Duplicate item found: %s" % item)
        else:
            Redis.hset("duplicate", item['scene_name'], 1)
            return item


# 数据库操作
class DBPipeline(object):
    def __init__(self):
        self.session = DBSession()

    def process_item(self, item, spider):
        sql = Scene(
            scene_name=item["scene_name"],
            web_site=item["web_site"],
            creat_time=item["creat_time"],
            )
        self.session.add(sql)
        self.session.commit()

    def close_spider(self, spider):
        self.session.close()

