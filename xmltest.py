from xml.dom.minidom import parseString

strxml = "<Camera><Trigger>25</Trigger><template>1</template><direction>1</direction></Camera>"

returnxml = "<Camera><return><state>1001</state><X>1.11</X><Y>2.22</Y><Z>3.33</Z><A>4.44</A><B>5.55</B><C>6.66</C><result>1</result><lables>101</lables></return></Camera>"


def cmdreturn(code, euler, result, labels):
    if len(euler) == 6:
        return "<Camera><return><state>{}</state>" \
               "<X>{:.2f}</X><Y>{:.2f}</Y><Z>{:.2f}</Z><A>{:.2f}</A>" \
               "<B>{:.2f}</B><C>{:.2f}</C><result>{}</result>" \
               "<lables>{}</lables></return></Camera>" \
            .format(code, euler[0], euler[1], euler[2], euler[3], euler[4], euler[5], result, labels)


def cmdget(strxml):
    try:
        doc = parseString(strxml)
        collection = doc.documentElement
        Trigger = collection.getElementsByTagName("Trigger")[0].childNodes[0].data
        template = collection.getElementsByTagName("template")[0].childNodes[0].data
        direction = collection.getElementsByTagName("direction")[0].childNodes[0].data
        data = {}
        data["Trigger"] = Trigger
        data["template"] = template
        data["direction"] = direction
    except Exception as e:
        data = {}
    return data




if __name__ == '__main__':
    print(cmdget(strxml))
    euler = (1.11,2.22,3.33,4.44,5.55,6.66)
    print(cmdreturn(1001,euler,1,2))

# #coding=utf-8
#
# #通过minidom解析xml文件
# import xml.dom.minidom as xmldom
# import os
# '''
# XML文件读取
# <?xml version="1.0" encoding="utf-8"?>
# <catalog>
#     <maxid>4</maxid>
#     <login username="pytest" passwd='123456'>dasdas
#         <caption>Python</caption>
#         <item id="4">
#             <caption>测试</caption>
#         </item>
#     </login>
#     <item id="2">
#         <caption>Zope</caption>
#     </item>
# </catalog>
#
# '''
#
# xmlfilepath = os.path.abspath("test.xml")
# print ("xml文件路径：", xmlfilepath)
#
# # 得到文档对象
# domobj = xmldom.parse(xmlfilepath)
# print("xmldom.parse:", type(domobj))
# # 得到元素对象
# elementobj = domobj.documentElement
# print ("domobj.documentElement:", type(elementobj))
#
# #获得子标签
# subElementObj = elementobj.getElementsByTagName("login")
# print ("getElementsByTagName:", type(subElementObj))
#
# print (len(subElementObj))
# # 获得标签属性值
# print (subElementObj[0].getAttribute("username"))
# print (subElementObj[0].getAttribute("passwd"))
#
# #区分相同标签名的标签
# subElementObj1 = elementobj.getElementsByTagName("caption")
# for i in range(len(subElementObj1)):
#     print ("subElementObj1[i]:", type(subElementObj1[i]))
#     print (subElementObj1[i].firstChild.data)  #显示标签对之间的数据
