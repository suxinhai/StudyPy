# -*- coding: utf-8 -*-
# @Time : 3/16/2022 9:12 AM
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net

"""
知识点一：
当一个进程启动之后，会默认产生一个主线程，因为线程是程序执行流的最小单元，当设置多线程时，主线程会创建多个子线程，
在python中，默认情况下（其实就是setDaemon(False)），主线程执行完自己的任务以后，就退出了，此时子线程会继续执行自己的任务，直到自己的任务结束，例子见下面一。

知识点二：
当我们使用setDaemon(True)方法，设置子线程为守护线程时，主线程一旦执行结束，则全部线程全部被终止执行，
可能出现的情况就是，子线程的任务还没有完全执行结束，就被迫停止，例子见下面二。

知识点三：
此时join的作用就凸显出来了，join所完成的工作就是线程同步，即主线程任务结束之后，进入阻塞状态，一直等待其他的子线程执行结束之后，主线程在终止，例子见下面三。
"""

from queue import Queue, Empty
from threading import Thread
from time import sleep


def printonehundrud(n):
    for i in range(n):
        print(i)


class multiThread:
    THREAD_POOL_SIZE = 0

    def __init__(self, adapter, method, size):
        self.adapter = adapter
        self.THREAD_POOL_SIZE = size
        self.method = method
        self.work_queue = Queue()
        self.threads = [Thread(target=self.worker, args=(self.work_queue,)) for _ in range(self.THREAD_POOL_SIZE)]
        for thread in self.threads:
            thread.start()
        # self.work_queue.join()
        # while self.threads:
        # self.threads.pop().join()

    def worker(self, work_queue):
        while not self.adapter.is_stop_adapter:
            try:
                item = work_queue.get(block=True)
            except Empty:
                break
            else:
                self.method(item)
                work_queue.task_done()


if __name__ == '__main__':
    threads = multiThread(printonehundrud, 4)
    threads.work_queue.put(100)
    threads.work_queue.put(200)
    threads.work_queue.put(300)
    threads.work_queue.put(400)
