# -*- coding: utf-8 -*-
# @Time : 2022/2/17 19:48
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net

from time import sleep
import threading

class a:
    def __init__(self,queue):
        self.queue = queue
        threading.Thread(target=self.start).start()

    def start(self):
        while True:
            msg = self.queue.get(block=True)
            print(msg)
            sleep(1)



