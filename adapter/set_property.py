from unified_service.caller import HubCaller
import threading
import logging
import grpc
import json
import time

HUB_ADDRESS = '127.0.0.1:5307'


class adapter():
    def __init__(self, *args):
        super().__init__(*args)
        self.is_stop_adapter = False
        self.hub_caller = HubCaller(HUB_ADDRESS)

    def call(self, service_name, message, timeout=None):
        if message.get("function") != 'getDigitalIn':
            logging.info("Call service:{}, message:{}".format(service_name, message))
        if not hasattr(HubCaller, "is_supports_timeout"):  # Just for forward compatible
            return self.hub_caller.call("forward", {"name": service_name, "message": message})
        else:
            return self.hub_caller.call("forward", {"name": service_name, "message": message}, timeout=timeout)

    def call_viz(self, func_name, msg={}, timeout=None):
        msg["function"] = func_name
        return self.call("executor", msg, timeout)

    def wait_viz_result(self, msg, timeout=None):
        try:
            logging.info("Run Mech-Viz:{}".format(msg))
            self.reply = json.loads(self.call_viz("run", msg, timeout).decode())
        except grpc._channel._Rendezvous as e:
            self.reply = e.details().split("=")[2][:-20]
            logging.info("Run Mech-Viz:{}".format(msg))
            return
        except Exception as e:
            logging.exception("Unknown exception from Mech-Viz: {}".format(e))
            return
        logging.info(self.reply)

    def set_task_property(self, msg, timeout=None):
        return self.call_viz("setTaskProperties", msg, timeout)

    def read_task_property(self, msg, timeout=None):
        result = self.call_viz("readProperties", msg, timeout)
        logging.info("Property result: {}".format(result))
        return result

    def call_vision(self, func_name, msg={}, project_name=None, timeout=None):
        msg["function"] = func_name
        service_name = project_name if project_name else self.vision_project_name
        try:
            return self.call(service_name, msg, timeout)
        except grpc.FutureTimeoutError as e:
            logging.error(e)
            return "{}".encode()

    def set_step_property(self, msg, project_name=None, timeout=None):
        return self.call_vision("setStepProperties", msg, project_name, timeout)

    def read_step_property(self, msg, project_name=None, timeout=None):
        result = self.call_vision("readProperties", msg, project_name, timeout)
        logging.info("Property result: {}".format(result))
        return result

    def read_di_task_property(self, timeout=None):
        msg = {"name": "2" + "_M",
               "properties": ['diListToCheck']}
        result = self.call_viz("readProperties", msg, timeout)
        logging.info("Property result: {}".format(result))
        return result

    def read_visual_move_property(self, name, property):
        msg = {"name": name,
               "properties": [property]}
        info = json.loads(self.read_task_property(msg).decode())
        return info

    def get_info_from_visual_move(self):
        edgeCornerLabelNumber = self.read_visual_move_property("2" + "_M", "edgeCornerLabelNumber")
        objOffsetInSuckerX = self.read_visual_move_property("2" + "_M", "objOffsetInSuckerX")
        objOffsetInSuckerY = self.read_visual_move_property("2" + "_M", "objOffsetInSuckerY")
        return edgeCornerLabelNumber, objOffsetInSuckerX, objOffsetInSuckerY

    def set_move_pallet(self, name, key):
        msg = {"name": name, "values": {"startIndex": key}}
        return self.set_task_property(msg)

    def set_branch(self, name, area):
        time.sleep(0.2)  # 这里延迟1s是需要等Viz执行器完全启动
        try:
            info = {"out_port": area, "other_info": []}
            msg = {"name": name,
                   "values": {"info": json.dumps(info)}}
            self.set_task_property(msg)
        except Exception as e:
            logging.exception(e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    a = adapter()
    msg = {"simulate": True, "project_dir": "D:/projects/projects/北京三快科技-美团送药-药袋分拣【P21030805】/new_viz",
           "keep_exec_state": False, "save_executor_data": False}
    # reply = json.loads(a.call_viz("run", msg, None).decode())
    t = threading.Thread(target=a.wait_viz_result, args=(msg, None))
    t.start()
    # try:
    #     ret = a.set_task_property(
    #         {'name': 'notify_1', 'values': {'serviceName': '{}'.format("asdf"), 'message': 'started'}})
    #     logging.info(ret)
    # except Exception as e:
    #     logging.error(e)
    time.sleep(5)
    a.set_move_pallet("123", 3)
    time.sleep(5)
    a.set_branch("321", 0)

    t.join()
