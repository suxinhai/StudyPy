# -*- coding: utf-8 -*-
"""
redis连接类的实现，redis连接的单例实现
"""
import redis
import json


def convert(data):
    if isinstance(data, bytes):  return data.decode()
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    return data


class RedisConnector(object):
    """redis连接类，提供redis相关的读写接口"""

    def __init__(self, host, port=6379, db=None):
        self.conn = redis.StrictRedis(host=host, port=port, db=db, socket_timeout=60000, client_name="suxinhai")

    def get(self, key):
        result = self.conn.get(key)
        if result is not None:
            result = eval(result)
        return result

    def get_bytes(self, key):
        return self.conn.get(key)

    def set(self, key, value, timeout=None):
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value)
        self.conn.set(key, value)
        if timeout:
            self.conn.expire(key, timeout)

    def mod(self, key, value):
        result = self.conn.get(key)
        if result:
            result2 = self.conn.set(key, value)
            print('redis更新结果:%s' % result2)
        else:
            print("key " + key + "is not found")

    def remove(self, key):
        result = self.conn.delete(key)

    def close(self):
        # clinet_list = self.conn.client_list()
        # client = None
        # for one in clinet_list:
        #     if one.get("name") == "suxinhai":
        #         client = one.get("addr")
        # self.conn.client_kill(client)
        self.conn.connection_pool.disconnect()

    def self_lpush(self, queue_name, msg):
        """
        将任务写入队列
        :param queue_name:
        :param msg: dict, 当前任务要写入的队列,
        :return: int,
        """
        message = {'msg': msg}
        bytes_msg = bytes(str(message), 'utf-8')
        self.conn.lpush(queue_name, bytes_msg)
        return 1

    # 此push方法供下游推数据使用
    def lpush(self, queue_name, msg_dict):
        try:
            self.conn.lpush(queue_name, json.dumps(msg_dict))
            return True
        except Exception as e:
            return False

    # 设置哈希型数据结构
    def hset(self, name, key, value):
        try:
            self.conn.hset(name, key, value)
            return True
        except Exception as e:
            return False

    # 删除hash某key
    def hdel(self, name, key):
        try:
            self.conn.hdel(name, key)
            return True
        except Exception as e:
            return False

    def hkeys(self, name):

        res_list = self.conn.hkeys(name)
        return [convert(i) for i in res_list]

    # 是否存在hash某key
    def hexists(self, name, key):

        return self.conn.hexists(name, key)

    # 获取hash某value
    def hget(self, name, key):
        try:
            res_vaule = self.conn.hget(name, key)
            return res_vaule.decode()
        except Exception as e:
            return None

    # 弹出下游数据
    def blpop(self, queue_name):

        res = self.conn.blpop(queue_name)[1]
        return json.loads(res)

    def brpop(self, queue_name):

        res = self.conn.brpop(queue_name)[1]
        return json.loads(res)

    def rpush(self, queue_name, msg):
        """
        将任务写入队列,
        :param queue_name:
        :param msg: dict, 当前任务要写入的队列,
        :return: uuid,
        """
        message = {'msg': msg}
        bytes_msg = bytes(str(message), 'utf-8')
        self.conn.rpush(queue_name, bytes_msg)
        return 1



