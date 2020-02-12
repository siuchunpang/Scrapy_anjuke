from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:root@localhost:3306/spider?charset=utf8')

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


# 初始化redis数据库连接
# 加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型
# Redis = redis.StrictRedis(host='localhost', port=6379, db=1, decode_responses=True)

# 使用redis连接池
pool = redis.ConnectionPool(host='localhost', port=6379, db=1, decode_responses=True)
Redis = redis.StrictRedis(connection_pool=pool)
