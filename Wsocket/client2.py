# -*- coding: utf-8 -*-
# @Time : 3/25/2022 2:56 PM
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net

from websocket import create_connection
from time import sleep
import threading


class WebsocketAdapter:

    def __init__(self):
        self._server = create_connection("ws://127.0.0.1:5678")

    def send(self, msg):
        if self._server.connected:
            self._server.send(msg)

    def start(self):
        # self.before_start_adapter()
        # while not self.is_stop_adapter:
        while True:
            try:
                if not self._server.connected:
                    self._server = create_connection("ws://127.0.0.1:5678")
                cmds = self._server.recv()
                # logging.info("Recv raw data:{}".format(cmds))
            except Exception as e:
                self._server.close()
                print("收包错误")
                print(e)
                continue
                # logging.exception("Exception occurred when recving: {}".format(e))
            else:
                try:
                    self.handle_command(cmds)
                except Exception as e:
                    print("处理错误错误")
                    print(e)
                    # self.msg_signal.emit(logging.ERROR,
                    #                      _translate("messages", "Handle command exception: {}".format(e)))
                    # logging.exception("Adapter exception in handle_command(): {}".format(e))

    def handle_command(self, e):
        print(e)


if __name__ == '__main__':
    adapter = WebsocketAdapter()
    try:
        adapter.start()
    except Exception as e:
        print('start')
        print(e)
