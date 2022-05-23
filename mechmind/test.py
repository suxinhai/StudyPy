# -*- coding: utf-8 -*-
# @Time : 4/7/2022 3:06 PM
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
from struct import unpack, pack


def floatToBytes(f):
    bs = pack(">f", f)
    return "{} {} {} {}".format(hex(bs[0]), hex(bs[1]), hex(bs[2]), hex(bs[3]))


def intToBytes(i):
    bs = pack(">i", i)
    return "{} {} {} {}".format(hex(bs[0]), hex(bs[1]), hex(bs[2]), hex(bs[3]))


if __name__ == '__main__':
    while True:
        print("请输入数字")
        key = input()
        if "." in str(key):
            print(floatToBytes(float(key)))
        else:
            print(intToBytes(int(key)))
