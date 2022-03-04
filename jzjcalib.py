import json
import logging
import math
import sys
from struct import pack, unpack
from time import sleep
import threading
import os
import modbus_tk
from modbus_tk import modbus_tcp
import random

# host = "192.168.1.13"
host = "127.0.0.1"

slaveid = 1


class jzjcalib:

    def __init__(self):
        self.num = 0
        self.master = modbus_tcp.TcpMaster(host=host, port=502)

    def read_data_int(self, starting_address):
        return self.master.execute(slave=slaveid,
                                   function_code=modbus_tk.defines.READ_HOLDING_REGISTERS,
                                   starting_address=starting_address,
                                   quantity_of_x=1)[0]

    def read_data_float(self, starting_address):
        return_data = self.master.execute(slave=slaveid,
                                          function_code=modbus_tk.defines.READ_HOLDING_REGISTERS,
                                          starting_address=starting_address,
                                          quantity_of_x=2, data_format=">f")
        byte_data = self.floatToBytes(return_data[0])
        return self.bytesToFloat(byte_data[0], byte_data[1], byte_data[2], byte_data[3])

    def write_data_int(self, starting_address, output_value):
        self.master.execute(slaveid, modbus_tk.defines.WRITE_SINGLE_REGISTER, starting_address=starting_address,
                            quantity_of_x=1,
                            output_value=output_value)

    def write_data_float(self, starting_address, output_value):
        self.master.execute(slaveid, modbus_tk.defines.WRITE_MULTIPLE_REGISTERS, starting_address=starting_address,
                            quantity_of_x=2,
                            output_value=unpack("<HH", pack("f", output_value)))

    def floatToBytes(self, f):
        bs = pack("f", f)
        return bs[3], bs[2], bs[1], bs[0]

    def bytesToFloat(self, h1, h2, h3, h4):
        ba = bytearray()
        ba.append(h3)
        ba.append(h4)
        ba.append(h1)
        ba.append(h2)
        return unpack("!f", ba)[0]

    def robot_run(self):
        self.write_data_int(1002 - 1, 1)
        print('机器人开始运动')
        pass

    def send_robot_jps(self, jps_num, jps):
        self.write_data_int(1010 - 1 + (jps_num - 1) * 20, 0)
        self.write_data_int(1011 - 1 + (jps_num - 1) * 20, 0)
        for i, j in enumerate(jps):
            self.write_data_float(1012 - 1 + (jps_num - 1) * 20 + 2 * (i + 1 - 1), float('{:.3f}'.format(j)))

    def test(self):
        while True:
            print("请输入机器人的6个jps:")
            cmd = self.get_tickets()
            if len(cmd) != 6:
                continue
            if cmd[0] == 'exit':
                break
            self.send_robot_jps(1, cmd)
            self.write_data_int(1003 - 1, 1)
            numnow = random.randint(1, 25)
            if self.num != numnow:
                self.num = numnow
            else:
                numnow += 1
            self.write_data_int(1004 - 1, numnow)
            self.write_data_int(1001 - 1, 2)
            self.robot_run()

    def get_tickets(self):
        tickets_list = []
        print('Please input tickets number:\n')
        for ticket in input().split(','):
            tickets_list.append(float(ticket))
        return tickets_list


if __name__ == '__main__':
    jzjcalib().test()
