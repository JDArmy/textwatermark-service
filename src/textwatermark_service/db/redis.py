"""redis database connection"""

import redis

redis_db = redis.StrictRedis(host="redis", port=6379, db=0)
