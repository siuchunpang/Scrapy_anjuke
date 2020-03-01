from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class Scene(Base):
    __tablename__ = 'scene'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    scene_unique_name = Column(String)
    scene_name = Column(String)
    web_site = Column(String)
    link_3d = Column(String)
    creat_time = Column(DateTime)
    shoot_count = Column(Integer)


class SceneImg(Base):
    __tablename__ = 'scene_img'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    scene_id = Column(Integer, ForeignKey("scene.id"))
    img_url = Column(String)
    is_downloaded = Column(String)
    failed_download_reason = Column(String)

