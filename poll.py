# -*- coding: utf-8 -*-
# @Time : 2022/1/21 14:01
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
import modbus_tk
from modbus_tk import modbus_tcp
from struct import pack, unpack


class poll:

    def __init__(self, HOST, PORT):
        self.master = modbus_tcp.TcpMaster(host=HOST, port=PORT)

    def read_data_int(self, slaveid, starting_address):
        return self.master.execute(slave=slaveid,
                                   function_code=modbus_tk.defines.READ_HOLDING_REGISTERS,
                                   starting_address=starting_address,
                                   quantity_of_x=1)[0]

    def read_data_float(self, slaveid, starting_address, sequence):
        return_data = self.master.execute(slave=slaveid,
                                          function_code=modbus_tk.defines.READ_HOLDING_REGISTERS,
                                          starting_address=starting_address,
                                          quantity_of_x=2, data_format=">f")
        # data_format=">f"
        byte_data = self.floatToBytes(return_data[0])
        return self.bytesToFloat(*byte_data, sequence)

    def write_data_int(self, slaveid, starting_address, output_value):
        self.master.execute(slaveid, modbus_tk.defines.WRITE_SINGLE_REGISTER, starting_address=starting_address,
                            quantity_of_x=1,
                            output_value=output_value)

    def write_data_float(self, slaveid, starting_address, output_value, sequence):
        byte_data = self.floatToBytes(output_value)
        output_value = self.bytesToFloat(*byte_data, sequence)
        self.master.execute(slaveid, modbus_tk.defines.WRITE_MULTIPLE_REGISTERS, starting_address=starting_address,
                            quantity_of_x=2,
                            output_value=(output_value,), data_format='>f')

    def get_sequence(self, params):
        ba = bytearray()
        for i in params[4]:
            if i == "A":
                ba.append(params[0])
            if i == "B":
                ba.append(params[1])
            if i == "C":
                ba.append(params[2])
            if i == "D":
                ba.append(params[3])
        return ba

    def floatToBytes(self, f):
        bs = pack("f", f)
        return bs[3], bs[2], bs[1], bs[0]

    def bytesToFloat(self, *params):

        ba = self.get_sequence(params)
        return unpack("!f", ba)[0]


if __name__ == '__main__':
    poll1 = poll("127.0.0.1", 502)
    res = poll1.read_data_float(1, 0, "CDAB")
    print(res)
