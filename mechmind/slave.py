# -*- coding: utf-8 -*-
# @Time : 2022/1/21 14:01
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
from modbus_tk import modbus_tcp, defines
import modbus_tk
import modbus_tk.modbus
import modbus_tk.modbus_tcp
from struct import unpack, pack

"""
需要创建初始化寄存
"""


class Slave:
    def __init__(self, HOST, PORT):
        self.slave = None
        self.start_server(HOST, PORT)

    def init_4x_register(self, address, number):
        self.slave_1.add_block('block1', modbus_tk.defines.READ_HOLDING_REGISTERS, address, number)
        self.slave_1.set_values('block1', address, number * [0])

    def init_3x_register(self, address, number):
        self.slave_1.add_block('block2', modbus_tk.defines.HOLDING_REGISTERS, address, number)
        self.slave_1.set_values('block2', address, number * [0])

    def start_server(self, HOST, PORT):
        self.server = modbus_tk.modbus_tcp.TcpServer(port=PORT, address=HOST, timeout_in_sec=3)
        self.server.start()
        self.slave_1 = self.server.add_slave(1)

    def read_register_I_4x(self, address, quantity_of_x=1):
        return self.slave_1.get_values('block1', address, quantity_of_x)[0]

    def write_register_I_4x(self, address, output_value=0):
        self.slave_1.set_values('block1', address, output_value)

    def read_register_I_3x(self, address, quantity_of_x=1):
        return self.slave_1.get_values('block2', address, quantity_of_x)[0]

    def write_register_I_3x(self, address, output_value=0):
        self.slave_1.set_values('block2', address, output_value)

    def write_register_F_4x(self, address, value, sequence):
        byte_data = self.floatToBytes(value)
        output_value = self.bytesToFloat(*byte_data, sequence)
        int_value = unpack('<HH', pack('>f', output_value))
        self.slave_1.set_values('block1', address, int_value)

    def read_register_F_4x(self, address, sequence, quantity_of_x=2):
        byte_data = self.slave_1.get_values('block1', address, quantity_of_x)
        data = unpack('>BBBB', pack('<HH', *byte_data))
        out_put = self.bytesToFloat(*data, sequence)
        return out_put

    def get_sequence(self, params):
        ba = bytearray()
        for i in params[4]:
            if i == "B":
                ba.append(params[0])
            if i == "A":
                ba.append(params[1])
            if i == "D":
                ba.append(params[2])
            if i == "C":
                ba.append(params[3])
        return ba

    def floatToBytes(self, f):
        bs = pack("f", f)
        return bs[3], bs[2], bs[1], bs[0]

    def bytesToFloat(self, *params):
        ba = self.get_sequence(params)
        return unpack("!f", ba)[0]

    def stop(self):
        self.server.stop()


if __name__ == '__main__':
    ModBus = Slave("0.0.0.0", 503)
    ModBus.init_3x_register(5100, 20)
    ModBus.write_register_I_3x(5101, 1)
