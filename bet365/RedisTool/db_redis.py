# -*- coding: utf-8 -*-

import json
import redis


class RedisClient(object):
    def __init__(self, host, port, password, db):
        pool = redis.ConnectionPool(host=host, port=port, password=password, db=db)
        self._db = redis.StrictRedis(connection_pool=pool)

    def get(self, key):
        pass


class ProxyRedis(RedisClient):
    def __init__(self, host, port, password, db):
        super(ProxyRedis, self).__init__(host, port, password, db)

    def get(self, key):
        return self._db.lrange(key, 0, -1)
        # return self._db.smembers(key)


class MatchRedis(RedisClient):
    def __init__(self, host, port, password, db):
        super(MatchRedis, self).__init__(host, port, password, db)

    def save(self, dict_key, key, value):
        self._db.hset(dict_key, key, value)

    def exists(self, dict_key, key):
        return self._db.hexists(dict_key, key)

    def remove(self, dict_key, key):
        self._db.hdel(dict_key, key)

    def get(self, key):
        map_str = self._db.get(key)
        return json.loads(map_str) if map_str else []


class RedisFactory(object):
    def create_redis(self, name, host, port, password, db):
        redis_map = {'match': MatchRedis, 'proxy': ProxyRedis,}
        redis_class = redis_map.get(name, None)
        if redis_class:
            return redis_class(host, port, password, db)
        return None





