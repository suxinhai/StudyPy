from mechmind.wr import read_json_file

file_dir_path = "C:/Users/mech-mind/Desktop/"
"""
获取手动跺型的数量
"""


def get_manual_stack(file):
    total = 0
    content = read_json_file(file)
    layers = content.get('layers', '')
    layouts = content.get('layouts', '')
    layers_layoutUuid = [i.get('layoutUuid') for i in layers]
    layouts_layoutUuid = {i.get('layoutUuid', ''): len(i.get('positions', '')) for i in layouts}

    for i in layers_layoutUuid:
        if i in layouts_layoutUuid.keys():
            total += layouts_layoutUuid[i]
    return total


if __name__ == '__main__':
    print(get_manual_stack(file_dir_path + '7' + '.json'))
