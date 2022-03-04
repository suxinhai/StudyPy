# -*- coding: utf-8 -*-
# @Time : 2022/2/23 13:51
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
import queue

if __name__ == '__main__':
    q = queue.Queue()

    print(q.get())
    q.put("01")