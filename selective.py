# -*- coding: utf-8 -*-
# @Time : 2022/2/9 14:57
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
import random

students = ['张震(张震|Zhen Zhang)', '范兴安(范兴安 | Xingan Fan)', '张钧硕(张钧硕| Zhang Junshuo)', '董一鸣(董一鸣 |Yiming Dong)',
            '拱忠奇(拱忠奇丨Zhongqi Gong)', '邵志(邵志｜Zhi Shao)', '王雨峰(王雨峰 | Yufeng Wang)', '宋志伟(宋志伟 | Zhiwei Song)',
            '陈颂(陈颂|Song Chen)', '荆钊(荆钊 | Zhao Jing)', '赵博(赵博｜Bo Zhao)', '胡冰(胡冰 | Bing Hu)', '李章宏(李章宏|Zhang hong Li)',
            '刘信勇(刘信勇｜Xinyong Liu)', '张志军(张志军 | Zhijun Zhang)', '王旭(王旭|Xu Wang)', '高俊龙(高俊龙｜Junlong Gao)',
            '李勐(李勐｜Meng Li)', '樊方(樊方|Fang FAN)', '张贝(张贝|Bei Zhang)', '廖光军(廖光军|Guangjun Liao)', '高金鑫(高金鑫 | Jinxin Gao)',
            '郭利飞(郭利飞 | Lifei Guo)', '王亚光(王亚光|Yaguang Wang)', '孙广浩(孙广浩丨Guanghao Sun)', '聂致强(聂致强| Zhiqiang Nie)',
            '刘超(刘超|Chao Liu)', '王其阳(王其阳｜Qiyang Wang)', '田亮(田亮 | Liang Tian)', '刘庆昊(刘庆昊｜Qinghao Liu)',
            '黄亚中(黄亚中｜Zhongya Huang)', '周永乐(周永乐|Yongle Zhou)', '张健(张健|Jian Zhang)', '王帅(王帅|Shuai Wang)',
            '张常龙(张常龙| Eric Zhang)', '蔡俊(蔡俊丨Jun Cai)', '龚望为(龚望为 | Wangwei Gong)']

if __name__ == '__main__':
    student = random.choice(students)
    print(student)