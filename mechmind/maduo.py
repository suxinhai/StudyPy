import json

def parseJson(String):
    start = str.find(String, '{')
    reversed_String = ''.join(reversed(String))
    end = len(String) - str.find(reversed_String, '}')
    return String[start+1:end-1]




def matrix_transposition(data):
    # 2维矩阵转置
    return list(map(list, zip(*data)))

def sort_pallet_seq(seq):
    box_types = []
    box_poses = []
    box_sizes = []
    box_pallet_indexs = []
    for i, pickbox in enumerate(seq):

        # 整合数据
        box_poses.append(pickbox['pose']['translation'])
        box_types.append(pickbox['property']['type'])
        box_sizes.append(pickbox['size'])
        box_pallet_indexs.append(pickbox['pose']['palletIndex'])
    return pack_box_seq(box_types, box_poses, box_sizes, box_pallet_indexs)

def pack_box_seq(box_types, box_poses, box_sizes, box_pallet_indexs):
    bundle = matrix_transposition([box_types, box_poses, box_sizes, box_pallet_indexs])
    box_seq = []
    key = ["type", 'pose','size','palletIndex']
    for i in range(len(bundle)):
        box_seq.append(dict(zip(key, bundle[i])))
    return box_seq

def order_generater(json_order):
    order = {}
    order["isStack"] = True
    boxData = []
    for one in json_order:
        boxData.append(one)
    order["boxData"] = boxData
    return order


if __name__ == '__main__':
    String = "1，{{'quantity': 3.0, 'size': [427.0, 286.0, 201.0], 'type': '100891'},{'quantity':5.0, 'size': [327.0, 250.0, 200.0], 'type': '100211'}}，1.2，1.2"
    print(parseJson(String))
    print(eval(parseJson(String)))
    print(order_generater(eval(parseJson(String))))

    name = '出库区混码_autoMiddlePoint'
    print(name.find('1'))
