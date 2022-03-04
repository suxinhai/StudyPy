# -*- coding: utf-8 -*-
# @Time : 2022/1/24 13:13
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
import logging
import sys
from time import sleep
import threading
from snap7 import util as siemens_util, client as siemens_client
import subprocess
import os
from os import path, listdir, remove

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from util import json_keys as jk
from util.util_file import read_json_file
from util.setting_file import mmind_path, adapter_dir, setting_file, sys_settings
from ui.settings import get_auto_load_projects, update_robot_setting_from_viz, robot_type_in_viz_project, \
    get_robot_dof_and_dh, BackgroundProgramSetting, RobotServerSetting

ROBOT_SERVER_MAIN_FILE = path.abspath(
    path.join(path.dirname(__file__), "..", "..", "Mech_RobServ", "src", "main.py")).replace("\\", "/")
ROBOT_SERVER_MAIN_FILE_INTERNAL = path.abspath(
    path.join(path.dirname(__file__), "..", "..", "..", "Mech_RobServ", "src", "main.py")).replace("\\", "/")
ROBOT_PARAMS_FILE = "/resource/robot/robot_params.json"
ROBOT_CLIENTS_FILE = "robot_clients.json"

LOCAL_HUB_ADDRESS = "127.0.0.1:5307"


class ConRobot(object):

    def __init__(self, adapter):
        try:
            self.sub_process_list = {}
            self.adapter = adapter
            self.load_settings()
            self.start = False
            self.stop = False
            self.robot_name = ""
            self.robot_server_setting = None
            self.robot_server_process = None
            self.background_setting = None
            sleep(8)
            threading.Thread(target=self.start_read).start()
        except Exception as e:
            logging.error(e)

    def load_settings(self):
        self.load_robot_server_settings()

    def load_robot_server_settings(self):
        settings = read_json_file(setting_file)
        self.robot_server_setting = RobotServerSetting(settings.get(jk.robot_server, {}))
        self.background_setting = BackgroundProgramSetting(settings.get(jk.background_program, {}))
        update_robot_setting_from_viz(self.background_setting, self.robot_server_setting)
        robot_type = self.robot_server_setting.type
        self.robot_name = robot_type

    def start_robserver(self):
        robot_server_setting = self.robot_server_setting
        robot_type = robot_server_setting.type
        self.robot_name = robot_type
        start_cmd = ["python", robot_server_setting.robserver_file, LOCAL_HUB_ADDRESS, robot_server_setting.ip,
                     robot_type,
                     robot_type, str(robot_server_setting.dof), str(robot_server_setting.dh_d1)]
        self.robot_server_process = subprocess.Popen(start_cmd)
        logging.info("Start robot server:{}".format(start_cmd))

    def stop_robserver(self):
        if not self.robot_server_process:
            return
        self.robot_server_process.terminate()
        logging.info("stop robot server")

        """
        重写
        """

    def connect_robot(self):
        self.start_robserver()

    def get_start(self):
        return False

    def get_stop(self):
        return False

    def get_connect(self):
        return True

    def start_read(self):
        while not self.adapter.is_stop_adapter:
            print("机器人准备好：{},开始：{}，停止 ：{}".format(self.get_connect(), self.get_start(), self.get_stop()))
            if self.get_connect():
                if not self.adapter.find_services(self.robot_name):
                    self.connect_robot()
                sleep(2)
        self.stop_robserver()
