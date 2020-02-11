from anjukespider.model.scene import Scene
from anjukespider.model.config import DBSession


class DBPipeline(object):
    def open_spider(self, spider):
        self.session = DBSession()

    def process_item(self, item, spider):
        sql = Scene(
            scene_name=item["scene_name"].encode("utf-8"),
            web_site=item["web_site"],
            creat_time=item["creat_time"].encode("utf-8"),
            )
        self.session.add(sql)
        self.session.commit()

    # 关闭数据库连接
    def close_spider(self, spider):
        self.session.close()
