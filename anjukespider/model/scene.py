from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class Scene(Base):
    __tablename__ = 'scene'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    scene_name = Column(String)
    web_site = Column(String)
    link_3d = Column(String)
    creat_time = Column(DateTime)
