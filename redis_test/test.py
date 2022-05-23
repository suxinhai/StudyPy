# -*- coding: utf-8 -*-
# @Time : 4/15/2022 9:43 AM
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
from redis_test.redisconn import RedisConnector
from time import sleep
import threading

WORK_STATION_NAME = "A-1"
EXCEPTION_LOCK = "Exception/lock"


class test:
    def __init__(self):
        self.hard_status = False
        self.task_manager = RedisConnector(host="106.14.150.21", port=26379, db=2)  # 任务收发的redis接口
        threading.Thread(target=self.add).start()

    def is_task_error(self):
        except_error = self.task_manager.hget(EXCEPTION_LOCK, WORK_STATION_NAME)
        if except_error:
            soft_status, hard_status = except_error.split("_")
            if hard_status == "1":
                self.hard_status = True
            else:
                self.hard_status = False
            if soft_status == "0":
                return False
        return True

    def add(self):
        while True:
            key = input()
            if key == "1":
                self.task_manager.hset(EXCEPTION_LOCK, WORK_STATION_NAME, "0_0")


if __name__ == '__main__':
    demo = test()
    demo.task_manager.hset(EXCEPTION_LOCK, WORK_STATION_NAME, "1_0")
    while True:
        if not demo.is_task_error():
            break
        sleep(1)
    print("关锁")
