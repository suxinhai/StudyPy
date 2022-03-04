# -*- coding: utf-8 -*-
# @Time : 2022/2/17 19:48
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
from Queuetest import queue1
import queue

class b:
    def __init__(self):
        self.queue = queue.Queue()

        self.aa = queue1.a(self.queue)
        self.queue.put("1")

if __name__ == '__main__':
    b()