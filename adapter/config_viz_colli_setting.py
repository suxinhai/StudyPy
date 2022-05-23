from unified_service.caller import HubCaller
import json
import time


# from utils import printAndLog

def setColliConfig(hub_caller, record_collision_contacts, compute_complete_collision):
    msg = {"function": "setConfig",
           "record_collision_contacts": record_collision_contacts,
           "compute_complete_collision": compute_complete_collision}
    hub_caller.call("forward", {"name": "executor", "message": msg})
    print("setting colli config as :{} ".format(msg))


if __name__ == '__main__':
    hub_caller = HubCaller('127.0.0.1:5307')
    # setColliConfig(hub_caller,sys.argv[1],sys.argv[2])
    setColliConfig(hub_caller, False, False)
