import os

model_dict = {}
model_code_dict = {}

vision_dict = {'2': 'vision_test'}
label_code_dict = {'4': '0'}
model_properties_dict = {'多模板粗匹配': ['pickpoint', 'model', 'label'],
                         '多模板精匹配': ['pickpoint', 'model', 'label']}

model_name = {'pickpoint': 'geometryCenterFile', 'model': 'modelFile', 'label': 'modelLabelFile'}


def parse_model():
    global model_dict
    global model_code_dict
    model_dict = {}
    model_code_dict = {}
    model_dir = 'D:/projects/model'
    geometrycenterfile = 'pickpoint'
    modellabelfile = 'label'
    modelfile = 'model'
    for model_type in os.listdir(model_dir):
        model_type_dir = os.path.join(model_dir, model_type)
        if not os.path.isdir(model_type_dir):
            continue
        # 如果发现文件夹名字中带_，则认为是需要类型码，格式是：类型码_类型
        index = model_type.find('_')
        if index > 0:
            code, real_type = model_type.split('_')[0], model_type[index + 1:]
            model_code_dict[real_type] = code
        else:
            real_type = model_type
        infos = {}
        infos[modelfile] = ''
        infos[geometrycenterfile] = ''
        infos[modellabelfile] = ''
        for file_name in os.listdir(model_type_dir):
            file_path = os.path.join(model_type_dir, file_name).replace("\\", "/")
            if not os.path.isfile(file_path):
                continue
            name = file_name.split('.')[0].lower()

            if modelfile in name:
                infos[modelfile] = infos[modelfile] + ';' + file_path
            if modellabelfile in name:
                infos[modellabelfile] = infos[modellabelfile] + ';' + file_path
            if geometrycenterfile in name:
                infos[geometrycenterfile] = infos[geometrycenterfile] + ';' + file_path

        model_dict[real_type] = infos
        infos[modelfile] = infos[modelfile][1:]
        infos[modellabelfile] = infos[modellabelfile][1:]
        infos[geometrycenterfile] = infos[geometrycenterfile][1:]
    print("Model map: {}".format(model_dict))
    print("Model code map: {}".format(model_code_dict))


def step_message(step_name, values):
    msg = {"name": step_name,
           "values": values}
    return msg


def get_model_type_by_code(code):
    for k, v in model_code_dict.items():
        if v == code:
            return k


def set_step(model_type):
    for name, properties in model_properties_dict.items():
        values = {}
        for p in properties:
            values[model_name[p]] = model_dict[model_type][p.lower()]
        print(step_message(name, values))


if __name__ == '__main__':
    f = open("out.yml", "w")
    print('111', file=f)
