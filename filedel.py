
# -*- coding: utf-8 -*-
# @Time : 2022/2/25 9:28
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
import os
import shutil
from time import sleep

LOCAL_SHARE_DIR = r"D:\vision\shareFiles\1"

BAK_DIR = r"D:\TASK"

# 单板线寻边工位：1
STATION_NUM = 1
# 配置一：是否需要寻边，1为需要，0为不需要

def get_is_need_corner():
    if STATION_NUM == 1:
        return 1
    if STATION_NUM == 2:
        return 0
    if STATION_NUM == 3:
        return 0

IS_NEED_CORNER = get_is_need_corner()

if __name__ == '__main__':
    print(IS_NEED_CORNER)