import cbor2
import json
import os


def read_file(file, encoding='utf-8'):
    try:
        with open(file, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(e)


def read_json_file(file, encoding='utf-8'):
    contents = read_file(file, encoding)
    if not contents:
        return {}
    try:
        return json.loads(contents)
    except Exception:
        return {}


def read_binary_file(file, mode='rb+'):
    try:
        with open(file, mode) as f:
            return f.read()
    except Exception:
        pass


def read_cbor_file(file, mode='rb+'):
    try:
        with open(file, mode) as f:
            return cbor2.load(f)
    except Exception:
        pass


def write_file(file, contents, encoding='utf-8'):
    try:
        with open(file, 'w', encoding=encoding) as f:
            f.write(contents)
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        return str(e)


def write_json_file(file, js, encoding='utf-8'):
    return write_file(file, json.dumps(js, sort_keys=True, indent=4, separators=(",", ": ")), encoding)


def write_binary_file(file, contents, mode='wb+'):
    try:
        with open(file, mode) as f:
            f.write(contents)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    dict_n = "{'Offline': {'offlineOrder': [{'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [147.5, 137.5, 43]}, 'property': {'tagOnLongEdge': False, 'type': 'a', 'weight': 0}, 'size': [80, 100, 43]}, {'pose': {'orientation': 2, 'palletIndex': 0, 'translation': [52.5, 147.5, 43]}, 'property': {'tagOnLongEdge': False, 'type': 'a', 'weight': 0}, 'size': [100, 80, 43]}, {'pose': {'orientation': 2, 'palletIndex': 0, 'translation': [137.5, 42.5, 43]}, 'property': {'tagOnLongEdge': False, 'type': 'a', 'weight': 0}, 'size': [100, 80, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [42.5, 52.5, 43]}, 'property': {'tagOnLongEdge': False, 'type': 'a', 'weight': 0}, 'size': [80, 100, 43]}, {'pose': {'orientation': 2, 'palletIndex': 0, 'translation': [242.5, 142.5, 43]}, 'property': {'tagOnLongEdge': False, 'type': 'e', 'weight': 0}, 'size': [100, 90, 43]}, {'pose': {'orientation': 2, 'palletIndex': 0, 'translation': [242.5, 47.5, 43]}, 'property': {'tagOnLongEdge': False, 'type': 'e', 'weight': 0}, 'size': [100, 90, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [37.5, 242.5, 43]}, 'property': {'tagOnLongEdge': False, 'type': 'b', 'weight': 0}, 'size': [70, 100, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [112.5, 242.5, 43]}, 'property': {'tagOnLongEdge': False, 'type': 'b', 'weight': 0}, 'size': [70, 100, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [187.5, 242.5, 43]}, 'property': {'tagOnLongEdge': False, 'type': 'b', 'weight': 0}, 'size': [70, 100, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [262.5, 242.5, 43]}, 'property': {'tagOnLongEdge': False, 'type': 'b', 'weight': 0}, 'size': [70, 100, 43]}, {'pose': {'orientation': 2, 'palletIndex': 0, 'translation': [157.5, 42.5, 86]}, 'property': {'tagOnLongEdge': False, 'type': 'a', 'weight': 0}, 'size': [100, 80, 43]}, {'pose': {'orientation': 2, 'palletIndex': 0, 'translation': [52.5, 42.5, 86]}, 'property': {'tagOnLongEdge': False, 'type': 'a', 'weight': 0}, 'size': [100, 80, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [142.5, 137.5, 86]}, 'property': {'tagOnLongEdge': False, 'type': 'e', 'weight': 0}, 'size': [90, 100, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [47.5, 137.5, 86]}, 'property': {'tagOnLongEdge': False, 'type': 'e', 'weight': 0}, 'size': [90, 100, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [142.5, 242.5, 86]}, 'property': {'tagOnLongEdge': False, 'type': 'e', 'weight': 0}, 'size': [90, 100, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [47.5, 242.5, 86]}, 'property': {'tagOnLongEdge': False, 'type': 'e', 'weight': 0}, 'size': [90, 100, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [252.5, 52.5, 86]}, 'property': {'tagOnLongEdge': False, 'type': 'a', 'weight': 0}, 'size': [80, 100, 43]}, {'pose': {'orientation': 2, 'palletIndex': 0, 'translation': [242.5, 152.5, 86]}, 'property': {'tagOnLongEdge': False, 'type': 'e', 'weight': 0}, 'size': [100, 90, 43]}, {'pose': {'orientation': 2, 'palletIndex': 0, 'translation': [242.5, 247.5, 86]}, 'property': {'tagOnLongEdge': False, 'type': 'e', 'weight': 0}, 'size': [100, 90, 43]}, {'pose': {'orientation': 2, 'palletIndex': 0, 'translation': [117.5, 42.5, 129]}, 'property': {'tagOnLongEdge': False, 'type': 'a', 'weight': 0}, 'size': [100, 80, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [42.5, 147.5, 129]}, 'property': {'tagOnLongEdge': False, 'type': 'c', 'weight': 0}, 'size': [80, 80, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [127.5, 147.5, 129]}, 'property': {'tagOnLongEdge': False, 'type': 'c', 'weight': 0}, 'size': [80, 80, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [42.5, 232.5, 129]}, 'property': {'tagOnLongEdge': False, 'type': 'c', 'weight': 0}, 'size': [80, 80, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [212.5, 147.5, 129]}, 'property': {'tagOnLongEdge': False, 'type': 'c', 'weight': 0}, 'size': [80, 80, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [127.5, 232.5, 129]}, 'property': {'tagOnLongEdge': False, 'type': 'c', 'weight': 0}, 'size': [80, 80, 43]}, {'pose': {'orientation': 4, 'palletIndex': 0, 'translation': [212.5, 232.5, 129]}, 'property': {'tagOnLongEdge': False, 'type': 'c', 'weight': 0}, 'size': [80, 80, 43]}]}}"
    json_n = json.loads(dict_n)
    print(json_n)
