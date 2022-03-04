import socket
import struct
import threading
import logging
import uuid
import json
import time
import snap7
from time import sleep
import os
import sys
import re
import http.client
from adapter.adapter import HttpServerAdapter
# from adapter.P1912DA233.params import *
from unified_service.json_service import JsonService
from unified_service.json_service import start_server
from adapter.services import NotifyService, register_service, JsonService, start_server, RobotService

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from adapter.P1912DA233 import params
from util.util_file import read_json_file
import urllib
import urllib.request

# WMS_ADDRESS = "22.16.24.85:8089"
WMS_ADDRESS = "22.16.24.85:8089"
PLC_ADDRESS = '192.168.1.50'
WMS_ROBOT_URL = '/iwms/robotMsg'
WMS_PLC_URL = '/iwms/placeMsg'
WMS_BOXNOTEXIST = '/iwms/boxNotExist'

VIZ_PROJECT_DIR = r'D:\projects\projects\智联弘盛二期\Viz-钱箱拆码垛-Fanuc'

HOST_ADDRESS = "0.0.0.0:8000"
HUB_ADDRESS = "127.0.0.1:5307"
ROBOT_NAME = "FANUC_R1000IA_100F"

HTTP_REQUEST = 'HTTP/1.1 200 OK\n\n%s'
HTTP_HEADERS = {"Content-type": "application/json"}

DB_NUM = 4
STRING_LEN = 10

WCS_NEW_URL = '/iwms/plcBCReturnSingle'

WCS_INPUT_RETURN_SIGNAL = '/iwms/inputReturnSignal'

WCS_BUTTON_URL = '/iwms/buttonReturnSignal'

# 入库偏移地址
STATION_OFFSET = {
    "A": 20,  # 入库_A端允许放箱
    "B": 24,  # 入库_B端箱子到位
    "C": 28  # 入库_C端箱子到位
}

# 出库偏移地址
STATION_OFFSET_2 = {
    "A": 22,  # 出库_A端箱子到位
    "B": 26,  # 出库_B端允许放箱
    "C": 30  # 出库_C端允许放箱
}

# 收到对方指令，我们给WMS的反馈
data_response = {
    "reqCode": "",
    "stCode": 0,
    "msg": ""
}

req_response = {
    "reqCode": "",
    "stCode": 0,
    "cargo": "",  # 是否有货
    "msg": ""
}

# 发送到/iwms/robotMsg的报文
# count是wms发给我们的拆码垛数量
# stackCount是我们自己拆码垛的计数
send_to_wms = {
    "reqCode": "",
    "reqTime": "",
    "taskCode": 1,
    "stCode": 0,
    "errorType": 0,
    "taskNo": "",
    "count": 0,
    "stackCount": 0
}

plc_send = {
    "reqCode": "",
    "reqTime": "",
    "taskNo": 0,
    "location": ""
}

send_no_box = {
    "reqCode": "",
    "reqTime": "",
    "location": ""
}


def add_generate_dict(upload_json):
    upload_json['reqCode'] = str(uuid.uuid4())
    upload_json['reqTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


class AdapterService(JsonService):
    service_name = "adapter_notify"
    service_type = "notify"

    def __init__(self, _handle_notify_message):
        self.lock = threading.Lock()
        self.handle_notify_message = _handle_notify_message

    def notify(self, request, _):
        msg = request["notify_message"]
        logging.info("notify message:{}".format(msg))

        with self.lock:
            self.handle_notify_message(msg)


class P1912DA233Adapter(HttpServerAdapter):
    viz_project_dir = VIZ_PROJECT_DIR
    # is_simulate = True

    is_force_real_run = True

    def __init__(self, address):
        super().__init__(address)
        self.check_list = []
        self.check_list_bc = []
        self.cmd_func_dict = {params.RESET: self.reset,
                              params.INPUT: self.input_handler,
                              params.OUTPUT: self.output_handler,
                              params.B_REQ: self.b_station_req,
                              params.C_REQ: self.c_station_req,
                              params.CONF: self.set_conf,
                              params.SCROLLWHEEL: self.scrollWheel,
                              params.BC_RETURN: self.wms_return_bc,
                              params.ENABLE_BTN: self.wms_entable_btn}
        self._register_service()
        # self.check_list = []

        self.download_json = dict()
        self.robot_down_json = dict()
        self.check_box_json = dict()  # 主动给WMS发到位信息
        self.check_no_box_json = dict()
        self.req_respones_json = dict()
        self.robot_send_json = dict()

        self.robot_send_json = send_to_wms
        self.check_box_json = plc_send
        self.check_no_box_json = send_no_box

        self.req_respones_json = req_response
        self.current_task = None

        self.plc_once = snap7.client.Client()
        self.plc_once.disconnect()
        self.plc_once.connect(PLC_ADDRESS, 0, 1)

        self.plc_bc = snap7.client.Client()
        self.plc_bc.disconnect()
        self.plc_bc.connect(PLC_ADDRESS, 0, 1)

        self.plc_input = snap7.client.Client()
        self.plc_input.disconnect()
        self.plc_input.connect(PLC_ADDRESS, 0, 1)

        self.plc_output = snap7.client.Client()
        self.plc_output.disconnect()
        self.plc_output.connect(PLC_ADDRESS, 0, 1)

        self.plc_bc_return = snap7.client.Client()
        self.plc_bc_return.disconnect()
        self.plc_bc_return.connect(PLC_ADDRESS, 0, 1)

        self.plc_button_return = snap7.client.Client()
        self.plc_button_return.disconnect()
        self.plc_button_return.connect(PLC_ADDRESS, 0, 1)

        self.success_stack_num = -1

        self.stop_watch_input = True
        self.stop_watch_output = True
        self.RET_scrollwheel = False
        self.RET_scrollwheel_chu = False
        self.clr_box_last = {}
        self.clr_interval_last = {}
        self.ret = False
        self.ret_input = False
        self.lock = threading.Lock()  # 多线程操作同一个list时需要加锁
        logging.info("adapter初始化")
        # threading.Thread(target=self.check_in_box_ready).start()
        threading.Thread(target=self.check_box_not_in_bc).start()
        threading.Thread(target=self.check_in_box_ready_input).start()
        threading.Thread(target=self.check_in_box_ready_output).start()
        # self.monitor_bc_return()
        threading.Thread(target=self.monitor_bc_return).start()
        threading.Thread(target=self.monitor_button_return).start()

    def wms_return_bc(self):
        location = self.download_json['location']
        if location == 'B':
            self.write_plc_data(offset=STATION_OFFSET["A"], value=True, data_type='Bool',
                                client=self.plc_bc_return, bit=2)
            sleep(1)
            self.write_plc_data(offset=STATION_OFFSET["A"], value=False, data_type='Bool',
                                client=self.plc_bc_return, bit=2)
        if location == 'C':
            self.write_plc_data(offset=STATION_OFFSET["A"], value=True, data_type='Bool',
                                client=self.plc_bc_return, bit=3)
            sleep(1)
            self.write_plc_data(offset=STATION_OFFSET["A"], value=False, data_type='Bool',
                                client=self.plc_bc_return, bit=3)
        data_response['reqCode'] = self.download_json['reqCode']
        data_response['stCode'] = 2000
        data_response['msg'] = ''
        data_to_send = HTTP_REQUEST % (json.dumps(data_response, ensure_ascii=False))
        self.send(data_to_send.encode())

    def wms_entable_btn(self):
        location = self.download_json['location']
        if location == 'B':
            self.write_plc_data(offset=STATION_OFFSET["B"], value=True, data_type='Bool',
                                client=self.plc_bc_return, bit=4)
            sleep(1)
            self.write_plc_data(offset=STATION_OFFSET["B"], value=False, data_type='Bool',
                                client=self.plc_bc_return, bit=4)
        if location == 'C':
            self.write_plc_data(offset=STATION_OFFSET["C"], value=True, data_type='Bool',
                                client=self.plc_bc_return, bit=4)
            sleep(1)
            self.write_plc_data(offset=STATION_OFFSET["C"], value=False, data_type='Bool',
                                client=self.plc_bc_return, bit=4)

        data_response['reqCode'] = self.download_json['reqCode']
        data_response['stCode'] = 2000
        data_response['msg'] = ''
        data_to_send = HTTP_REQUEST % (json.dumps(data_response, ensure_ascii=False))
        self.send(data_to_send.encode())


    def monitor_bc_return(self):
        ret_a = False
        ret_b = False
        ret_c = False

        while not self.is_stop_adapter:
            A = self.read_plc_data(STATION_OFFSET["A"], 'Bool', self.plc_bc_return, bit=1)
            B = self.read_plc_data(STATION_OFFSET["B"], 'Bool', self.plc_bc_return, bit=3)
            C = self.read_plc_data(STATION_OFFSET["C"], 'Bool', self.plc_bc_return, bit=3)
            logging.info("A:{},B:{},C:{}".format(A, B, C))
            if A == ret_a:
                if A:
                    return_msg = {"location": "BC"}
                    self._send_to_wms(WCS_INPUT_RETURN_SIGNAL, return_msg)
                    #self.write_plc_data(offset=STATION_OFFSET["A"], value=False, data_type='Bool',
                    #                    client=self.plc_bc_return, bit=1)
                ret_a = not A
            if B == ret_b:
                if B:
                    return_msg = {"location": "B"}
                    self._send_to_wms(WCS_NEW_URL, return_msg)
                    #self.write_plc_data(offset=STATION_OFFSET["B"], value=False, data_type='Bool',
                    #                    client=self.plc_bc_return, bit=3)
                ret_b = not B
            if C == ret_c:
                if C:
                    return_msg = {"location": "C"}
                    self._send_to_wms(WCS_NEW_URL, return_msg)
                    #self.write_plc_data(offset=STATION_OFFSET["C"], value=False, data_type='Bool',
                    #                    client=self.plc_bc_return, bit=3)
                ret_c = not C

    def monitor_button_return(self):
        ret_b = False
        ret_c = False
        while True:
            B = self.read_plc_data(24, 'Bool', self.plc_button_return, 2)
            C = self.read_plc_data(28, 'Bool', self.plc_button_return, 2)
            logging.info("B_button:{},C_button:{}".format(B, C))
            if B == ret_b:
                if B:
                    return_msg = {"location": "B"}
                    self._send_to_wms(WCS_BUTTON_URL, return_msg)
                ret_b = not B
            if C == ret_c:
                if C:
                    return_msg = {"location": "C"}
                    self._send_to_wms(WCS_BUTTON_URL, return_msg)
                ret_c = not C

    def _register_service(self):
        self.adapter_service = AdapterService(self.handle_notify_message)
        self.server, port = register_service(self.hub_caller, self.adapter_service)

    def handle_command(self, cmds):
        logging.info("RECV cmds : {}".format(cmds))
        self.download_json = self.unpack_command(cmds)
        logging.info('Receive cmds from WMS:{}'.format(self.download_json))
        self.current_task = self.download_json['api']
        if self.current_task not in params.valid_commands:
            data_response['stCode'] = 4000
            data_response['msg'] = 'Invalid request'
            data_to_send = HTTP_REQUEST % (json.dumps(data_response, ensure_ascii=False))
            self.send(data_to_send.encode())
            return
        try:
            self.cmd_func_dict[self.current_task]()
        except Exception as e:
            logging.exception(e)

    def init_upload_json(self):
        self.robot_send_json['taskCode'] = -1
        self.robot_send_json['stCode'] = -1
        self.robot_send_json['taskNo'] = ""
        self.robot_send_json['count'] = -1
        self.robot_send_json['stackCount'] = -1
        self.robot_send_json['errorType'] = 0
        self.success_stack_num = 0

        self.check_box_json['taskNo'] = ""
        self.check_box_json['location'] = ""
        self.check_no_box_json['location'] = ""

    def pack_robot_json(self):
        add_generate_dict(self.robot_send_json)
        self.robot_send_json['taskCode'] = self.robot_down_json['taskCode']
        self.robot_send_json['taskNo'] = self.robot_down_json['taskNo']
        self.robot_send_json['count'] = self.robot_down_json['count']

    def handle_notify_message(self, msg):
        # 出入库API
        if msg == 'main_cycle_notify':
            logging.info("api:{}".format(self.robot_down_json['api']))
            if self.robot_down_json['api'] == 'input':
                self.call_branch('branch_main', 0)  # 入库
                self.set_counter_property("counter_2", self.download_json['count'] - 1)
            else:
                self.call_branch('branch_main', 1)  # 出库
                self.set_counter_property("counter_3", self.download_json['count'] - 1)

        elif msg == 'check_plc_1':  # 入库检测A端
            self.write_plc_data(offset=2, value=1, data_type='Int', client=self.plc_once)  # 输送线正转
            self.write_plc_data(offset=14, value=True, data_type='Bool', client=self.plc_once)  # 触发A
            self.write_plc_data(offset=16, value=True, data_type='Bool', client=self.plc_once)  # 触发B
            self.write_plc_data(offset=18, value=True, data_type='Bool', client=self.plc_once)  # 触发C
            if self.read_plc_data(STATION_OFFSET["A"], 'Bool', self.plc_once):  # 入库_A端允许放箱
                self.call_branch('branch_enter', 0)
            else:
                self.call_branch('branch_enter', 1)
        elif msg == 'check_plc_2':  # 出库检测A端
            self.write_plc_data(offset=2, value=2, data_type='Int', client=self.plc_once)  # 输送线正转
            self.write_plc_data(offset=14, value=True, data_type='Bool', client=self.plc_once)  # 触发A
            self.write_plc_data(offset=16, value=True, data_type='Bool', client=self.plc_once)  # 触发B
            self.write_plc_data(offset=18, value=True, data_type='Bool', client=self.plc_once)  # 触发C
            if self.read_plc_data(STATION_OFFSET_2["A"], 'Bool', self.plc_once):  # 出库_A端箱子到位
                self.call_branch('branch_exit', 0)
            else:
                self.call_branch('branch_exit', 1)

        elif msg == 'single_finish_1':
            self.robot_send_json['reqCode'] = self.robot_down_json['reqCode']
            self.robot_send_json['reqTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.robot_send_json['taskCode'] = 1
            self.robot_send_json['stCode'] = 1
            self.robot_send_json['taskNo'] = self.robot_down_json['taskNo']
            self.robot_send_json['count'] = self.robot_down_json['count']
            self.robot_send_json['stackCount'] = 1
            self.success_stack_num += 1
            self.send_robot_msg_to_wms()
            logging.info("single_finish_1运行完成,入库单次码放成功，当前计数为：{}".format(self.success_stack_num))

        elif msg == 'single_finish_2':
            self.robot_send_json['reqCode'] = self.robot_down_json['reqCode']
            self.robot_send_json['reqTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.robot_send_json['taskCode'] = 2
            self.robot_send_json['stCode'] = 1
            self.robot_send_json['taskNo'] = self.robot_down_json['taskNo']
            self.robot_send_json['count'] = self.robot_down_json['count']
            self.robot_send_json['stackCount'] = 1
            self.success_stack_num += 1
            self.send_robot_msg_to_wms()
            logging.info("single_finish_2运行完成,出库单次码放成功，当前计数为：{}".format(self.success_stack_num))

        elif msg == 'single_fail_1':
            self.robot_send_json['reqCode'] = self.robot_down_json['reqCode']
            self.robot_send_json['reqTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.robot_send_json['taskCode'] = 1
            self.robot_send_json['stCode'] = 3
            self.robot_send_json['taskNo'] = self.robot_down_json['taskNo']
            self.robot_send_json['count'] = self.robot_down_json['count']
            self.robot_send_json['stackCount'] = 0
            logging.info("single_fail_1运行完成,入库单次码放失败，当前计数为：{}".format(self.success_stack_num))
            self.send_robot_msg_to_wms()

        elif msg == 'task_finish':
            if self.success_stack_num != self.robot_down_json['count']:
                self.robot_send_json['stCode'] = 4
                self.send_robot_msg_to_wms()  # 给wms发报文函数
                logging.info("总任务失败，码放数量与收到的数量不一致，总计数为：{}".format(self.success_stack_num))
            else:
                self.robot_send_json['stCode'] = 2
                self.send_robot_msg_to_wms()
                logging.info("总任务完成，码放数量与收到的数量一致，总计数为：{}".format(self.success_stack_num))

        elif msg in ('drop_bag_1', 'drop_bag_2'):
            self.robot_send_json['errorType'] = 2
            self.robot_send_json['stCode'] = 3
            logging.info("掉包报错")
            self.send_robot_msg_to_wms()

        elif msg in ('empty_put_1', 'empty_put_2'):
            self.robot_send_json['errorType'] = 1
            self.robot_send_json['stCode'] = 3
            logging.info("空抓报错")
            self.send_robot_msg_to_wms()

    def start_project(self):
        if self.start_viz(in_new_thread=True):
            data_response['reqCode'] = self.download_json['reqCode']
            data_response['stCode'] = 2000
            data_response['msg'] = '接收指令成功'
            data_to_send = HTTP_REQUEST % (json.dumps(data_response, ensure_ascii=False))
            self.send(data_to_send.encode())

        else:
            data_response['reqCode'] = self.download_json['reqCode']
            data_response['stCode'] = 4000
            data_response['msg'] = '失败，无效指令'
            data_to_send = HTTP_REQUEST % (json.dumps(data_response, ensure_ascii=False))
            self.send(data_to_send.encode())

    def input_handler(self):
        self.stop_watch_input = False
        self.stop_watch_output = True
        self.success_stack_num = 0
        # self.ret_input = True
        self.robot_down_json = self.download_json

        self.write_plc_data(offset=2, value=1, data_type='Int', client=self.plc_once)  # 输送线正转
        self.write_plc_data(offset=14, value=True, data_type='Bool', client=self.plc_once)  # 触发A
        self.write_plc_data(offset=16, value=True, data_type='Bool', client=self.plc_once)  # 触发B
        self.write_plc_data(offset=18, value=True, data_type='Bool', client=self.plc_once)  # 触发C
        self.start_project()

    def output_handler(self):
        # self.stop_watch_input = True
        # self.stop_watch_output = False
        self.success_stack_num = 0
        self.robot_down_json = self.download_json
        # self.ret = True
        # self.write_plc_data(offset=2, value=2, data_type='Int', client=self.plc_once)  # 输送线反转
        # self.write_plc_data(offset=16, value=True, data_type='Bool', client=self.plc_once)  # 触发B
        # self.write_plc_data(offset=18, value=True, data_type='Bool', client=self.plc_once)  # 触发C

        # with self.lock:
        #     # self.check_list = self.check_list + ['A']
        #     self.check_list = ['A']
        #     self.check_list_bc = ['B','C']
        self.start_project()
        # threading.Thread(target=self.check_in_box_ready_output).start()

    # 入库 主动监听BC点，只要到位就发1次
    # 出库 不主动监听，对面请求，我们读PLC的值给wms发送过去
    def b_station_req(self):  # 出库的时候用的
        if self.read_plc_data(STATION_OFFSET["B"], 'Bool', self.plc_once):
            logging.info("B点到位请求读取PLC成功，准备发送给WMS")
            self.req_respones_json["reqCode"] = self.download_json["reqCode"]
            self.req_respones_json["stCode"] = 2000
            self.req_respones_json["cargo"] = "true"
            self.req_respones_json["msg"] = "箱子已到请求点位"
            data_to_send = HTTP_REQUEST % (json.dumps(self.req_respones_json, ensure_ascii=False))
            self.send(data_to_send.encode())
            logging.info("B点到位请求发送给WMS成功，箱子已经到位，发送给WMS的信息为：{}".format(self.req_respones_json))
        else:
            self.req_respones_json["reqCode"] = self.download_json["reqCode"]
            self.req_respones_json["stCode"] = 2000
            self.req_respones_json["cargo"] = "false"
            self.req_respones_json["msg"] = "箱子未到请求点位"
            data_to_send = HTTP_REQUEST % (json.dumps(self.req_respones_json, ensure_ascii=False))
            self.send(data_to_send.encode())
            logging.info("B点到位请求发送给WMS成功，箱子未到位，发送给WMS的信息为：{}".format(self.req_respones_json))

    def c_station_req(self):
        if self.read_plc_data(STATION_OFFSET["C"], 'Bool', self.plc_once):
            logging.info("C点到位请求读取PLC成功，准备发送给WMS")
            self.req_respones_json["reqCode"] = self.download_json["reqCode"]
            self.req_respones_json["stCode"] = 2000
            self.req_respones_json["cargo"] = "true"
            self.req_respones_json["msg"] = "箱子已到请求点位"
            data_to_send = HTTP_REQUEST % (json.dumps(self.req_respones_json, ensure_ascii=False))
            self.send(data_to_send.encode())
            logging.info("C点到位请求发送给WMS成功，箱子已经到位，发送给WMS的信息为：{}".format(self.req_respones_json))

        else:
            self.req_respones_json["reqCode"] = self.download_json["reqCode"]
            self.req_respones_json["stCode"] = 2000
            self.req_respones_json["cargo"] = "false"
            self.req_respones_json["msg"] = "箱子未到请求点位"
            data_to_send = HTTP_REQUEST % (json.dumps(self.req_respones_json, ensure_ascii=False))
            self.send(data_to_send.encode())
            logging.info("C点到位请求发送给WMS成功，箱子未到位，发送给WMS的信息为：{}".format(self.req_respones_json))

    # 如果启用此函数，记得把output_handler函数中的反转操作注释掉
    def scrollWheel(self):
        if self.download_json['scrollWheelType'] == 2:
            self.write_plc_data(offset=2, value=2, data_type='Int', client=self.plc_once)  # 输送线反转
            self.write_plc_data(offset=14, value=True, data_type='Bool', client=self.plc_once)  # 触发A
            self.write_plc_data(offset=16, value=True, data_type='Bool', client=self.plc_once)  # 触发B
            self.write_plc_data(offset=18, value=True, data_type='Bool', client=self.plc_once)  # 触发C
            data_response['reqCode'] = self.download_json['reqCode']
            data_response['stCode'] = 2000
            data_response['msg'] = '设置成功，传送带切换为反转模式'
            data_to_send = HTTP_REQUEST % (json.dumps(data_response, ensure_ascii=False))
            self.send(data_to_send.encode())
            self.RET_scrollwheel = True
            self.stop_watch_input = True
            self.stop_watch_output = False
            self.ret = True
            self.clr_box_last = {'B': 0, 'C': 0}
            self.clr_interval_last = {'B': 0, 'C': 0}
            self.RET_scrollwheel = True
            self.RET_scrollwheel_chu = True
            logging.info("设置反转")
        else:
            data_response['reqCode'] = self.download_json['reqCode']
            data_response['stCode'] = 4000
            data_response['msg'] = '设置失败，请将传送带设置为反转模式'
            data_to_send = HTTP_REQUEST % (json.dumps(data_response, ensure_ascii=False))
            self.send(data_to_send.encode())
            logging.info("设置反转失败")
            self.RET_scrollwheel = True
            self.RET_scrollwheel_chu = True

    def check_in_box_ready_input(self):  # 入库检测BC端
        # 这三个变量相互关联，所以把INTERVAL也定义为变量，一起改不容易错
        logging.info("开始检查B、C点到位信息0")
        check_interval = 0.1  # unit: second
        # 箱子持续返回True的最少间隔次数, 防止没有箱子的时候传感器毛刺错误导致误识别为有箱子
        # 假如箱子最少持续1s, check_interval = 0.1，则会至少触发4次检测为True（注意不是5次）
        # 故实际对应箱子持续最小时间为 check_interval*(min_box+1)
        min_box = 10
        # 最小间隔时间，假如前后三次读传感器分别为true,false,true, 可以认为是传感器毛刺错误，应当认定为还是同一个箱子
        # 同上，对应最小间隔时间为 check_interval*(min_interval + 1)
        min_interval = 5
        # box_last = {}
        # interval_last = {}
        box_last = self.clr_box_last
        interval_last = self.clr_interval_last
        list_copy = ['B', 'C']
        logging.info("list_copy为：{}".format(list_copy))
        for check_item in list_copy:
            box_last[check_item] = 0
            interval_last[check_item] = 0
        # 这里可以设置一个成员变量控制 while not self.stop_watch:

        while not self.is_stop_adapter:
            logging.info("入库线程")
            logging.info("停止监测入库信号: {}".format(self.stop_watch_input))
            if self.ret_input:
                for check_item in list_copy:
                    box_last[check_item] = 0
                    interval_last[check_item] = 0
                    self.ret_input = False
            if self.RET_scrollwheel:
                for check_item in list_copy:
                    box_last[check_item] = 0
                    interval_last[check_item] = 0
                    self.RET_scrollwheel = False

            if not self.stop_watch_input:
                # print(list_copy)
                # while True:
                for check_item in list_copy:
                    # print(check_item)
                    # 入库时，BC端箱子到位时为True
                    has_box = self.read_plc_data(STATION_OFFSET[check_item], 'Bool', self.plc_input)
                    status_normal = self.read_plc_data(offset=4, data_type='Int', client=self.plc_input)
                    # logging.info("has_box: {}".format(has_box))
                    # logging.info("check_item: {}".format(check_item))
                    # logging.info("开始检查B、C点到位信息5")
                    logging.info("入库状态码：{}".format(status_normal))
                    logging.info("入库箱子：{}计数：{}".format(check_item, box_last[check_item]))
                    logging.info("入库B或C有无箱子：{}".format(has_box))
                    if self.RET_scrollwheel:
                        for check_item in list_copy:
                            box_last[check_item] = 0
                            interval_last[check_item] = 0
                            self.RET_scrollwheel = False

                    if has_box:
                        if status_normal == 0:
                            box_last[check_item] = box_last[check_item] + 1
                            if box_last[check_item] == min_box:
                                self.check_box_json['location'] = check_item
                                logging.info("入库流程——{}端箱子到位".format(check_item))
                                # logging.info("370行当前线程是：{}".format(threading.current_thread().ident))
                                # self.send_check_msg_to_wms()
                                threading.Thread(target=self.send_check_msg_to_wms).start()
                                logging.info("入库流程——{}端到位点发送完毕".format(check_item))
                            # 不可改成==，否则，容易导致误差累计，比如一个箱子持续时间比较久，几十秒，如果每几秒都有一次误判
                            # 那么容易导致最终interval_last累计足够导致即使有min_interval还是出错
                            if box_last[check_item] > min_box:
                                interval_last[check_item] = 0
                    else:
                        interval_last[check_item] = interval_last[check_item] + 1
                        if interval_last[check_item] > min_interval:
                            box_last[check_item] = 0
                sleep(check_interval)
            else:
                sleep(check_interval)

    def check_in_box_ready_output(self):  # 出库检测A端
        # 这三个变量相互关联，所以把INTERVAL也定义为变量，一起改不容易错
        check_interval = 0.1  # unit: second
        # 箱子持续返回True的最少间隔次数, 防止没有箱子的时候传感器毛刺错误导致误识别为有箱子
        # 假如箱子最少持续1s, check_interval = 0.1，则会至少触发4次检测为True（注意不是5次）
        # 故实际对应箱子持续最小时间为 check_interval*(min_box+1)
        min_box = 5
        # 最小间隔时间，假如前后三次读传感器分别为true,false,true, 可以认为是传感器毛刺错误，应当认定为还是同一个箱子
        # 同上，对应最小间隔时间为 check_interval*(min_interval + 1)
        min_interval = 2
        box_last = {}
        interval_last = {}
        # with self.lock:
        #     list_copy = self.check_list[:]
        list_copy = ['A']
        logging.info("list_copy为：{}".format(list_copy))
        for check_item in list_copy:
            box_last[check_item] = 0
            interval_last[check_item] = 0
        # 这里可以设置一个成员变量控制 while not self.stop_watch:

        while not self.is_stop_adapter:
            logging.info("出库线程:出库检测A点")
            logging.info("停止监测出库信号: {}".format(self.stop_watch_output))
            # while True:
            if not self.stop_watch_output:
                for check_item in list_copy:
                    # 出库时，A端箱子到位时为True
                    has_box = self.read_plc_data(STATION_OFFSET_2[check_item], 'Bool', self.plc_output)
                    status_normal = self.read_plc_data(offset=4, data_type='Int', client=self.plc_output)
                    logging.info("has_box: {}".format(has_box))
                    logging.info("status_normal: {}".format(status_normal))
                    logging.info("出库箱子：{}计数：{}".format(check_item, box_last[check_item]))
                    if has_box:
                        if status_normal == 0:
                            box_last[check_item] = box_last[check_item] + 1
                            if box_last[check_item] == min_box:
                                self.check_box_json['location'] = check_item
                                logging.info("出库流程——{}端箱子到位".format(check_item))
                                # logging.info("370行当前线程是：{}".format(threading.current_thread().ident))
                                # self.send_check_msg_to_wms()
                                threading.Thread(target=self.send_check_msg_to_wms).start()
                                logging.info("出库流程——{}端到位点发送完毕".format(check_item))
                            # 不可改成==，否则，容易导致误差累计，比如一个箱子持续时间比较久，几十秒，如果每几秒都有一次误判
                            # 那么容易导致最终interval_last累计足够导致即使有min_interval还是出错
                            if box_last[check_item] > min_box:
                                interval_last[check_item] = 0
                    else:
                        interval_last[check_item] = interval_last[check_item] + 1
                        if interval_last[check_item] > min_interval:
                            box_last[check_item] = 0
                sleep(check_interval)
            else:
                sleep(check_interval)

    def check_box_not_in_bc(self):  # 出库检测BC端
        # 这三个变量相互关联，所以把INTERVAL也定义为变量，一起改不容易错
        check_interval = 0.1  # unit: second
        # 箱子持续返回True的最少间隔次数, 防止没有箱子的时候传感器毛刺错误导致误识别为有箱子
        # 假如箱子最少持续1s, check_interval = 0.1，则会至少触发4次检测为True（注意不是5次）
        # 故实际对应箱子持续最小时间为 check_interval*(min_box+1)
        min_box = 5
        # 最小间隔时间，假如前后三次读传感器分别为true,false,true, 可以认为是传感器毛刺错误，应当认定为还是同一个箱子
        # 同上，对应最小间隔时间为 check_interval*(min_interval + 1)
        min_interval = 2
        box_last = {}
        interval_last = {}
        list_copy = ['B', 'C']
        logging.info("list_copy为：{}".format(list_copy))

        for check_item in list_copy:
            box_last[check_item] = 0
            interval_last[check_item] = 0
        # 这里可以设置一个成员变量控制 while not self.stop_watch:
        while not self.is_stop_adapter:
            logging.info("出库线程:出库检测BC点")
            if self.ret:
                for check_item in list_copy:
                    box_last[check_item] = 0
                    interval_last[check_item] = 0
                    self.ret = False

            if self.RET_scrollwheel_chu:
                for check_item in list_copy:
                    box_last[check_item] = 0
                    interval_last[check_item] = 0
                    self.RET_scrollwheel_chu = False
            if not self.stop_watch_output:
                # while True:
                # logging.info("开始检查B、C点到位信息3")
                for check_item in list_copy:
                    # 出库时，BC端没有箱子时为True
                    no_box = self.read_plc_data(STATION_OFFSET_2[check_item], 'Bool', self.plc_bc)
                    status_normal = self.read_plc_data(offset=4, data_type='Int', client=self.plc_bc)
                    # logging.info("BC点没有箱子：{}".format(has_box))
                    # logging.info("has_box: {}".format(has_box))
                    # logging.info("check_item: {}".format(check_item))
                    # logging.info("开始检查B、C点到位信息4")
                    logging.info("出库状态码：{}".format(status_normal))
                    logging.info("出库箱子：{}计数：{}".format(check_item, box_last[check_item]))
                    logging.info("出库{}端有无箱子：{}".format(check_item, not no_box))
                    if self.RET_scrollwheel_chu:
                        for check_item in list_copy:
                            box_last[check_item] = 0
                            interval_last[check_item] = 0
                            self.RET_scrollwheel_chu = False

                    if no_box:
                        if status_normal == 0:
                            box_last[check_item] = box_last[check_item] + 1

                            if box_last[check_item] == min_box:
                                self.check_no_box_json['location'] = check_item
                                logging.info("出库流程——{}端允许放箱".format(check_item))
                                # self.send_check_nobox_msg_to_wms()
                                threading.Thread(target=self.send_check_nobox_msg_to_wms).start()
                                logging.info("出库流程——{}端无箱状态发送完毕".format(check_item))
                            # 不可改成==，否则，容易导致误差累计，比如一个箱子持续时间比较久，几十秒，如果每几秒都有一次误判
                            # 那么容易导致最终interval_last累计足够导致即使有min_interval还是出错
                            if box_last[check_item] > min_box:
                                interval_last[check_item] = 0
                    else:
                        interval_last[check_item] = interval_last[check_item] + 1
                        if interval_last[check_item] > min_interval:
                            box_last[check_item] = 0
                sleep(check_interval)
            else:
                sleep(check_interval)

    def reset(self):
        self.init_upload_json()
        self.current_task = None
        data_response['reqCode'] = self.download_json['reqCode']
        data_response['stCode'] = 0000
        data_response['msg'] = '设置成功'
        data_to_send = HTTP_REQUEST % (json.dumps(data_response, ensure_ascii=False))
        self.send(data_to_send.encode())

    def set_conf(self):
        pass

        # 监听BC点，到位后发给WMS

    def send_check_msg_to_wms(self):
        add_generate_dict(self.check_box_json)
        self._send_to_wms(WMS_PLC_URL, self.check_box_json)

    def send_check_nobox_msg_to_wms(self):
        add_generate_dict(self.check_no_box_json)
        self._send_to_wms(WMS_BOXNOTEXIST, self.check_no_box_json)

    # single_fail, single_finish之类的主动给WMS发送使用的函数
    def send_robot_msg_to_wms(self):
        self.pack_robot_json()
        self._send_to_wms(WMS_ROBOT_URL, self.robot_send_json)

    def _send_to_wms(self, url, upload_json):
        con = http.client.HTTPConnection(WMS_ADDRESS)
        logging.info("send json:{}".format(upload_json))
        con.request('POST', url, json.dumps(upload_json), HTTP_HEADERS)
        res = con.getresponse()
        logging.info("recv：{}".format(res.read().decode()))

    @staticmethod
    def unpack_command(command):
        data = command.decode()
        logging.info("unpack_command data: {}".format(data))
        p1 = re.compile(r'[{](.*)[}]', re.S)
        data_list = re.findall(p1, data)
        data_string = '{%s}' % (data_list[0])
        data_dict = json.loads(data_string)
        logging.info("data_dict: {}".format(data_dict))
        return data_dict

    def call_branch(self, branch_name, out_port):
        info = {"out_port": out_port}
        msg = {"function": "setTaskProperties",
               "name": branch_name,
               "values": {"info": json.dumps(info)}}
        logging.info("call branch:{} {}".format(branch_name, out_port))
        self.call("executor", msg)

    def get_digital_in(self):
        di = json.loads(self.call(ROBOT_NAME, {"function": "getDigitalIn"}).decode())
        return int(di["value"])

    def set_digital_out(self, port, value):
        return self.call(ROBOT_NAME, {"function": "setDigitalOut", "port": port, "value": value})

    def set_counter_property(self, name, count):
        msg = {"name": name,
               "values": {"count": count}}
        self.set_task_property(msg)

    def read_plc_data(self, offset, data_type, client, bit=0, string_len=STRING_LEN, mode=0):
        data_type = str.capitalize(data_type)
        data_offset = {"Bool": 1, "Int": 2, "Real": 4, "String": string_len + 2}
        max_len = data_offset[data_type]
        # self.plc_once.connect(PLC_ADDRESS, 0, 1)
        if client.get_connected():
            data = client.db_read(DB_NUM, offset, max_len)
            # self.plc_once.disconnect()
            if data_type == 'Bool':
                value = snap7.util.get_bool(data, 0, bit)
            elif data_type == 'Int':
                value = snap7.util.get_int(data, 0)
            elif data_type == 'Real':
                value = snap7.util.get_real(data, 0)
            else:
                value = snap7.util.get_string(data, 0, max_len)
            return value if mode == 0 else (value, data)
            # return value
        else:
            logging.error("PLC is disconnected!")
            return

    def write_plc_data(self, offset, value, data_type, client, bit=0, string_len=STRING_LEN):
        data_type = str.capitalize(data_type)
        logging.info("set value:{}".format(value))
        _, byte_array = self.read_plc_data(offset, data_type, client, bit, string_len, mode=1)
        if data_type == 'Bool':
            snap7.util.set_bool(byte_array, 0, bit, value)
        elif data_type == 'Int':
            snap7.util.set_int(byte_array, 0, int(value))
        elif data_type == 'Real':
            snap7.util.set_real(byte_array, 0, float(value))
        else:
            snap7.util.set_string(byte_array, 0, value, string_len + 2)
        # self.plc_once.connect(PLC_ADDRESS, 0, 1)
        client.db_write(DB_NUM, offset, byte_array)
        # self.plc_once.disconnect()
        logging.info('PLC write successfully')
        # print('写入成功')
        return 0
        # return byte_array

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
#     server = P1912DA233Adapter(HOST_ADDRESS)
#     server.start()
