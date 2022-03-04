import os, sys
import math
# global definition
# base = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F]
from timeit import Timer

base = [str(x) for x in range(10)] + [chr(x) for x in range(ord('A'), ord('A') + 6)]


def dec2bin(string_num, count):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num, rem = divmod(num, 2)
        mid.append(base[rem])
    if len(mid) < count:
        return 0
    else:
        return mid[count - 1]


if __name__ == '__main__':
    pass