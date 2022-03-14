# -*- coding: utf-8 -*-
"""
@Auth ： 江宇旭
@Email ：jiang.yuxu@mech-mind.net
@Time ： 2021/12/1 16:27
"""
import logging
import time
from logging.handlers import TimedRotatingFileHandler
import os
import glob

BASE_DIR = r'D:'

class LogCreator(object):
    """
    log生成器，并按天/时/分/秒新建log,定时清理
    """
    def __init__(self, file_name):
        """
        :param file_name: str 日志文件的名称
        """
        self.file_name = file_name
        self.base_dir = BASE_DIR
        self.LogsPath = os.path.join(self.base_dir, 'log',
                                     '{0}-{1}.log'.format(file_name, time.strftime('%Y-%m-%d', time.localtime())))

        self.logger = logging.Logger(self.file_name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] [%(filename)s-line:%(lineno)d] %(message)s')
        # 按天存放 同类型log最多保留5个
        self.log_file_handler = TimedRotatingFileHandler(filename=self.LogsPath, when="midnight", interval=1,
                                                         backupCount=5,
                                                         encoding="utf-8")
        self.log_file_handler.setFormatter(formatter)
        self.logger.addHandler(self.log_file_handler)  # 输出到文件
        # 自动清理文件 同名文件保留设定定个数 其余删除
        self.auto_clear(5)

    def auto_clear(self, num):
        """
        自动清理log文件
        :param num: 同文件名(不包括日期)保留的文件个数
        :return:
        """
        file_list = sorted(glob.glob(os.path.join(self.base_dir, self.file_name + '*')),
                           key=lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(x))),
                           reverse=True)
        for file_ in file_list[num:]:
            os.remove(file_)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg,  *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

log_mechmind = LogCreator('mechmind') #系统日志，记录跟系统相关的一些日志，比如redis的启动host，端口等。不记录业务模块的日志


