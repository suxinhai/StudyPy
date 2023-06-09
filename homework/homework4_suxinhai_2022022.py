# -*- coding: utf-8 -*-
# @Time : 2022/2/22 12:36
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
c
from mechmind.wr import read_json_file

import dict2xml


def dict_to_xml(dict_in):
    xml_str = dict2xml.dict2xml(dict_in)
    print(xml_str)


file = r'python4.json'

if __name__ == '__main__':
    dic = read_json_file(file, encoding='UTF-8')
    dict_to_xml(dic)
