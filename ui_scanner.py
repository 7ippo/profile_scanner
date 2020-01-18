#encoding:utf-8

"""UI依赖资源数量扫描

扫描ui_setting/ui_setting_custom
输出各UI面板依赖的非公共资源数量与规模大小为json文件，方便后续展示报告

公共资源：指进入游戏后常驻内存的资源

output:

{
    "view_name1": {
        "icon" : { 
            "icon1" : [ width, height, size ],
            "icon2" : [ width, height, size ],
            ...
        },
        "atlas" : {
            "atlas1" : [ width, height, size ],
            "atlas2" : [ width, height, size ]
            ...
        },
        "count" : 2
    },
    "view_name2" : ...
}

authro: zpo

使用方法：
python ui_scanner.py [file_path]

options:
[file_path] ui_setting.json与ui_setting_custom.json的相对路径

"""

import os
import re
import argparse
import json
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('file_path', help='The path to ui_setting/ui_setting_custom.')

MAXRESOURCESREQUIRE = 6
RESOURCEPATH = "."
ATLASPATHPREFIX = "res/atlas"
PUBLICRESOURCES = {
        "rsl_btn",      # 按钮
        "rsl_num",      # 美术数字图片
        "rsl_other",    # 公用的美术图片
        "rsl_sliced",   # 背景图片
        "rsl_frame",    # 品质框
        "main_ui",      # 主界面
        "mainui_icon",  # 主界面图标
        "faces",        # 聊天表情
        "role_ip",      # 场景对象,仙位
        "fight_word",   # 场景对象,战斗飘字
        "attr_change",  # 场景对象,战斗飘字
        "buff",         # 场景对象,buff
        "common_window_view1",  # 公共面板
        # Loading底图
        "res/icon/login/login_bg.jpg",
        "res/icon/loading/loading_bg_1.jpg",
        "res/icon/loading/loading_bg_2.jpg",
        # 公共底板底图
        "res/icon/common_window_view1/bg.jpg",
        "res/icon/small_map/small_map.jpg",
        }

#TODO 读取资源详细信息，长宽，文件大小

def readIconOrAtlasDetail(res_name) -> dict:
    result = {}
    icon_re = re.compile(r'^res/icon')
    if icon_re.match(res_name):
        result[res_name] = []
        res_path = os.path.join(RESOURCEPATH, res_name)
        if os.path.exists(res_path):
            pic = Image.open(res_path)
            width, height = pic.size
            file_size = os.stat(res_path).st_size // 1024
            result[res_name] = [width , height, file_size]
        else:
            print("File: {} not exist! Please check ui_setting.".format(res_path))
            return result
    else:
        res_path = os.path.join(RESOURCEPATH, ATLASPATHPREFIX, res_name + '.atlas')
        if os.path.exists(res_path):
            with open(res_path, 'r', encoding='utf-8') as f:
                atlas_info = json.load(f)
                png_info = atlas_info["meta"]["image"]
                png_list = png_info.split(',')
                for png in png_list:
                    png_path = os.path.join(RESOURCEPATH, ATLASPATHPREFIX, png)
                    if os.path.exists(png_path):
                        pic = Image.open(png_path)
                        width, height = pic.size
                        file_size = os.stat(png_path).st_size //1024
                        result[png] = [width, height, file_size]
                    else:
                        print("File: {} not exist! Please check atlas {}.".format(png_path, res_path))
                        continue
        else:
            print("File: {} not exist! Please check ui_setting.".format(res_path))
            return result
    return result

#整合传入的ui配置文件与现有的非公共资源配置，去除公共资源后输出
def outputNonpublicRes(ui_setting, nonpublic_uisetting) -> dict:
    comment_re = re.compile(r'^//')
    icon_re = re.compile(r'^res/icon')
    for view_name in ui_setting:
        if comment_re.match(view_name) or len(ui_setting[view_name]) == 0:
            continue
        if view_name not in nonpublic_uisetting:
            nonpublic_uisetting[view_name] = {"icon":{},"atlas":{},"count":0}
        nonpublic_res = set(ui_setting[view_name]) - PUBLICRESOURCES
        for res in nonpublic_res:
            view_setting = nonpublic_uisetting[view_name]
            if icon_re.match(res):
                if res not in view_setting["icon"]:
                    res_info = readIconOrAtlasDetail(res)
                    view_setting["icon"].update(res_info)
                    view_setting["count"] += 1
            else:
                if res not in view_setting["atlas"]:
                    res_info = readIconOrAtlasDetail(res)
                    view_setting["atlas"].update(res_info)
                    view_setting["count"] += len(res_info.keys())
    return nonpublic_uisetting

if __name__ == '__main__':
    args = parser.parse_args()
    if not(args.file_path):
        parser.print_help()
        exit(0)
    ui_setting_path = os.path.join(args.file_path, 'ui_setting.json')
    ui_setting_custom_path = os.path.join(args.file_path, 'ui_setting_custom.json')
    ui_setting = {}
    ui_setting_custom = {}
    try:
        with open(ui_setting_path, 'r', encoding='utf-8') as f:
            ui_setting = json.load(f)
    except IOError:
        print("File: {} is not accessible.".format(ui_setting_path))
        exit(0)
    try:
        with open(ui_setting_custom_path, 'r', encoding='utf-8') as f:
            ui_setting_custom = json.load(f)
    except IOError:
        print("File: {} is not accessible.".format(args.file))
        exit(0)
    # 整合两个setting json，排除公共资源，输出一个面板所需的所有非公共资源
    nonpublic_uisetting = {}
    final_uisetting = outputNonpublicRes(ui_setting_custom, outputNonpublicRes(ui_setting, nonpublic_uisetting))
    
    with open("ui_setting_nonpublic.json", "w", encoding='utf-8') as f:
            json.dump(final_uisetting, f)
            print("ui_setting_nonpublic写入文件完成...")


    # 读取非公共资源信息，输出output.json
    # 大小：os.stat('whatever.png').st_size
    # 长宽:
    # im = Image.open('whatever.png')
    # width, height = im.size
    #TODO
