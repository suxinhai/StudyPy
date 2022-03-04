# -*- coding: utf-8 -*-
# @Time : 2022/1/26 17:17
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
"""
一、定义一个学生Student类。有下面的类属性：
1 姓名 name
2 年龄 age
3 成绩 score（语文，数学，英语) [每课成绩的类型为整数]


类方法：
1 获取学生的姓名：get_name() 返回类型:str
2 获取学生的年龄：get_age() 返回类型:int
3 返回3门科目中最高的分数。get_course() 返回类型:int


写好类以后，可以定义2个同学测试下:
zm = Student('zhangming',20,[69,88,100])
返回结果：
zhangming
20
100
"""

"""
二、定义一个字典类：dictclass。完成下面的功能：

dict = dictclass({你需要操作的字典对象})

1 删除某个key

del_dict(key)


2 判断某个键是否在字典里，如果在返回键对应的值，不存在则返回"not found"

get_dict(key)

3 返回键组成的列表：返回类型;(list)

get_key()

4 合并字典，并且返回合并后字典的values组成的列表。返回类型:(list)

update_dict({要合并的字典})
"""

"""
三、定义一个列表的操作类：Listinfo

包括的方法:

1 列表元素添加: add_key(keyname) [keyname:字符串或者整数类型]
2 列表元素取值：get_key(num) [num:整数类型]
3 列表合并：update_list(list) [list:列表类型]
4 删除并且返回最后一个元素：del_key()

a = Listinfo([44,222,111,333,454,'sss','333'])
"""


class Student:
    name = ""
    age = 0
    score = []

    def __init__(self, name, age, score):
        Student.name = name
        Student.age = age
        Student.score = score

    @classmethod
    def get_name(cls):
        return Student.name

    @classmethod
    def get_age(cls):
        return Student.age

    @classmethod
    def get_course(cls):
        return max(*Student.score)


class dictclass:

    def __init__(self, dict):
        self.dict = dict

    def del_dict(self, key):
        if self.dict.get(key):
            del self.dict[key]

    def get_dict(self, key):
        return self.dict[key] if self.dict.get(key) else "not found"

    def get_key(self):
        return list(self.dict.keys())

    def update_dict(self, net_dict):
        self.dict.update(net_dict)
        return list(self.dict.values())


class Listinfo:

    def __init__(self, List):
        self.List = List

    def add_key(self, keyname):
        self.List.append(keyname)

    def get_key(self, num):
        return self.List[num] if num < len(self.List) else "not exist"

    def update_list(self, List):
        return [self.List.append(one) for one in List]

    def del_key(self):
        if len(self.List) > 0:
            temp = self.List[-1]
            self.List.remove(self.List[-1])
            return temp
        else:
            return None



