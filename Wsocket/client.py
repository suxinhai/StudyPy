# -*- coding: utf-8 -*-
# @Time : 2022/3/4 9:35
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
import asyncio
import websockets
import threading
import time


# 向服务器端认证，用户名密码通过才能退出循环
async def auth_system(websocket):
    while True:
        cred_text = input("please enter your username and password: ")
        await websocket.send(cred_text)
        response_str = await websocket.recv()
        if "congratulation" in response_str:
            return True


async def send_msg(websocket):
    while True:
        print(1)
        await websocket.send("hello")
        await asyncio.sleep(1)


async def send():
    async with websockets.connect('ws://127.0.0.1:5678') as websocket:
        await send_msg(websocket)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send())
    loop.run_forever()
