# -*- coding: utf-8 -*-
# @Time : 2022/2/28 9:31
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net

def rec(key, json):
    if type(json) is dict:
        print('<%s>' % key)
        for key, value in json.items():
            rec(key, value)
        print('</%s>' % key)
    else:
        print('<%s>%s</%s>' % (key, json, key))


json = {
    "data": {
        "steel": {
            "steel_no": "TEST-A6",
            "model": "TEST-A84",
            "steel_width_px": 6500,
            "steel_width_mm": 6500,
            "steel_height_px": 5000,
            "steel_height_mm": 5000,
            "girder_sync_flag": 0,
            "station": "A301",
            "station_sn": -1
        },
        "feature_points": "null",
        "use_type": 2,
        "suckers": {
            "left_right": 1,
            "sucker_no": "AS41",
            "slide_no": 1,
            "grab_steel_x_px": 1643,
            "grab_steel_x_mm": 1643,
            "grab_steel_y_px": 2622,
            "grab_steel_y_mm": 2622,
            "grab_x_px": 1366,
            "grab_x_mm": 1356,
            "grab_y_px": 2062,
            "grab_y_mm": 2052,
            "magnetic_tool_type": 4,
            "grab_height": 8,
            "grab_rotation_angle": 0,
            "put_rotation_angle": 0,
            "cylinder_config": [
                0,
                0,
                31,
                -1,
                0,
                0,
                31,
                -1
            ],
            "magnetic_force_grade": 5
        },
        "take_pic_immediately": "true",
        "station_sn": -1,
        "station": "A301",
        "pallet": {
            "put_height_mm": 8,
            "put_y_mm": 3055.5,
            "is_first_used": 1,
            "put_rotation_angle": 0,
            "put_x_mm": 1360,
            "pallet": "AP41",
            "put_x_mm_old": 1356,
            "put_y_mm_old": 2052,
            "pallet_area_no": "1",
            "pallet_id": "AP41_121387375",
            "pallet_sn": 3,
            "is_sort": 1
        },
        "part_info": {
            "sort_no": 1,
            "part_model": "T-DD1",
            "part_weight": 100,
            "part_thickness": 8,
            "size_type": 3,
            "sort_type": 0,
            "bmp_path": "20211223115644287_returnPart.bmp",
            "scaling_factor": 1,
            "rect_top_left_x_px": 287,
            "rect_top_left_x_mm": 287,
            "rect_top_left_y_px": 570,
            "rect_top_left_y_mm": 570,
            "rect_width_px": 6000,
            "rect_width_mm": 6000,
            "rect_height_px": 4001,
            "rect_height_mm": 4001,
            "core_steel_x_px": 3265,
            "core_steel_x_mm": 3265,
            "core_steel_y_px": 2622,
            "core_steel_y_mm": 2622,
            "core_x_px": 2988,
            "core_x_mm": 2988,
            "core_y_px": 2062,
            "core_y_mm": 2062,
            "rotation_angle": 0,
            "standard_rect_width_px": 6000,
            "standard_rect_width_mm": 6000,
            "standard_rect_height_px": 4001,
            "standard_rect_height_mm": 4001,
            "standard_core_x_px": 3001,
            "standard_core_x_mm": 3001,
            "standard_core_y_px": 2013,
            "standard_core_y_mm": 2013
        }
    },
    "web_share_path": "\\\\192.168.1.102\\shareFiles\\A1\\",
    "message": "OK",
    "status": "0"
}

if __name__ == '__main__':
    rec("?xml version=\"1.0\"encoding=\"utf-8\"?", json)
