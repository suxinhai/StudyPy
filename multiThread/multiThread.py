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
import threading
from time import sleep
import os


def method():
    print(1)


class multiThread:
    THREAD_POOL_SIZE = 0

    def __init__(self, method, size):
        self.THREAD_POOL_SIZE = size
        self.filesize_dict = {}
        self.method = method
        self.work_queue = Queue()
        self.threads = [threading.Thread(target=self.worker, args=(self.work_queue,)) for _ in
                        range(self.THREAD_POOL_SIZE)]
        for thread in self.threads:
            thread.start()

    def worker(self, work_queue):
        while True:
            try:
                item = work_queue.get(block=True)
            except Empty:
                break
            else:
                # self.method(item)
                self.find_max_size_file(item)
                work_queue.task_done()

    def find_max_size_file(self, file):
        try:
            if os.path.isdir(file):
                files = os.listdir(file)
                for onefile in files:
                    file_path = os.path.join(file, onefile)
                    # print("{},{}".format(threading.current_thread().getName(), file_path))
                    self.work_queue.put(file_path)
            else:
                self.filesize_dict[file] = os.path.getsize(file)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    file_threads = multiThread(method, 10)
    file_threads.find_max_size_file(r"D:")

    file_threads.work_queue.join()
    # while file_threads.threads:
    #     file_threads.threads.pop().join()
