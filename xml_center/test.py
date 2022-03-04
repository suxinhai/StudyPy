# -*- coding: utf-8 -*-
# @Time : 2022/2/23 11:22
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
from wr import read_file
from xml.dom.minidom import parseString
import xmltodict

file = r"XML_KUKA_MM_VISION_2.xml"
GET_XML = '<ROBOT><TEL_ID>40</TEL_ID><M_ID>27</M_ID><J_ID>0</J_ID><POS X="1" Y="2" Z="3" A="1" B="2" C="3"></POS><PAR> Kalibrieren Ende : Ende#</PAR><T>#</T></ROBOT>'

RETURN_XML = "<VISION><TEL_ID>{}</TEL_ID><STAT_ID>{}</STAT_ID><ERR_ID>{}</ERR_ID><ERR_TEXT>{}</ERR_TEXT><POS1 X= '{}' Y= '{}' Z=  '{}' A=  '{}' B= '{}' C= '{}' ></POS><POS2 X= '{}' Y= '{}' Z=  '{}' A=  '{}' B= '{}' C= '{}' ></POS><POS3 X= '{}' Y= '{}' Z=  '{}' A=  '{}' B= '{}' C= '{}' ></POS><POS4 X= '{}' Y= '{}' Z=  '{}' A=  '{}' B= '{}' C= '{}' ></POS><POS5 X= '{}' Y= '{}' Z=  '{}' A=  '{}' B= '{}' C= '{}' ></POS><POS6 X= '{}' Y= '{}' Z=  '{}' A=  '{}' B= '{}' C= '{}' ></POS><POS7 X= '{}' Y= '{}' Z=  '{}' A=  '{}' B= '{}' C= '{}' ></POS><POS8 X= '{}' Y= '{}' Z=  '{}' A=  '{}' B= '{}' C= '{}' ></POS><POS9 X= '{}' Y= '{}' Z=  '{}' A=  '{}' B= '{}' C= '{}' ></POS><POS10 X= '{}' Y= '{}' Z=  '{}' A=  '{}' B= '{}' C= '{}' ></POS><PAR> Referenzieren : Go Next #</PAR><LABLE>{}</LABLE><POSNUM>{}</POSNUM><T>#</T></VISION>"

pos_list = ['X', 'Y', 'Z', 'A', 'B', 'C']


def cmdget(strxml):
    doc = parseString(strxml)
    collection = doc.documentElement
    ELEMENTS = collection.childNodes
    return_dict = {}
    for ELEMENT in ELEMENTS[:3]:
        key = ELEMENT.nodeName if len(ELEMENT.childNodes) > 0 else ""
        value = ELEMENT.childNodes[0].data if len(ELEMENT.childNodes) > 0 else ""
        return_dict[key] = value
    for i in range(6):
        value = ELEMENTS[3].getAttribute(pos_list[i])
        return_dict[pos_list[i]] = value
    for ELEMENT in ELEMENTS[4:]:
        key = ELEMENT.nodeName if len(ELEMENT.childNodes) > 0 else ""
        value = ELEMENT.childNodes[0].data if len(ELEMENT.childNodes) > 0 else ""
        return_dict[key] = value
    return return_dict


# def send_poses(code, send_complete, pose_count, visual_move_position, poses_send, labels_send,
#                speeds_to_send):
#
# def send_msg():
#


def return_cmd(code, send_complete, pose_count, visual_move_position, poses_send, labels_send,
               speeds_to_send):
    pass


if __name__ == '__main__':
    print(cmdget(GET_XML))
