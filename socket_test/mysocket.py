# -*- coding: utf-8 -*-
# @Time : 4/14/2022 10:48 AM
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
# 法一：
import socket
if __name__ == '__main__':
    socket.setdefaulttimeout(5)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 5678))
    sock.sendall('xxx'.encode())
    # 连接和接收的时候都设置一次超时
    try:
        sock.settimeout(5)
        sock.recv(1024)
    except socket.timeout:
        print(1)

    sock.close()