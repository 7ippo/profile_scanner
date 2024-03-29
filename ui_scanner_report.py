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
python ui_scanner.py

"""

import os
import re
import json
from PIL import Image
from pyecharts.components import Table
from pyecharts.charts import Tab
from pyecharts import options as opts

RESOURCEPATH = "."
ATLASPATHPREFIX = "res/atlas"
UISETTINGPATHPREFIX = "pre_load_config"
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
        "icon_goods",   # 物品图标
        # Loading底图
        "res/icon/login/login_bg.jpg",
        "res/icon/loading/loading_bg_1.jpg",
        "res/icon/loading/loading_bg_2.jpg",
        # 公共底板底图
        "res/icon/common_window_view1/bg.jpg",
        "res/icon/small_map/small_map.jpg",
        }

MAXATLASRESOURCE = 2
MAXUIRESOURCEWIDTH = 1024
ATLASIDENTIFIER = "--------------图集--------------"
ICONIDENTIFIER = "--------------icon--------------"
BLOCKIDENTIFIER = "\n"

# 总览图
"""
["AdventureRewardView", 
'------atlas------\nadventure.png\n------icon------\nres/icon/equip_star_icon/success_bg2.png\nres/icon/equip_star_icon/attr_bg.png\nres/icon/equip_star_icon/success_bg720.png\nres/icon/equip_star_icon/success_bg1.png\n',
'\n244 x 48\n409 x 106\n720 x 409\n196 x 54\n\n1024 x 1024',
'\n18\n1\n118\n13\n\n597', 
6]
"""
def table_base(data) -> Table:
    table = Table()
    headers = ["面板名称", "依赖资源", "宽 x 高", "大小(kb)", "网络请求数量"]
    table.add(headers, data).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="报告总览", subtitle="以网络请求数量降序排列")
    )
    return table

# 依赖图集数量超标
"""
["AdventureRewardView", 
'------atlas------\nadventure.png',
\n1024 x 1024]
"""
def table_atlas(data) -> Table:
    table = Table()
    headers = ["面板名称", "依赖图集", "宽 x 高"]
    table.add(headers, data).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="依赖图集数量超标", subtitle="标准是除公共图集外最多依赖2张图集")
    )
    return table

# 资源宽高超标
"""
["AdventureRewardView", 
'------atlas------\nadventure.png',
\n1024 x 1024,
'\n597']
"""
def table_size(data) -> Table:
    table = Table()
    headers = ["面板名称", "依赖资源", "宽 x 高", "大小(kb)"]
    table.add(headers, data).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="资源宽高超标", subtitle="标准是1024x1024")
    )
    return table

# 传入面板数据，组装成绘图数据
def get_row_for_base(name, ui_data) -> tuple:
    base_result = [] # 总览图数据
    atlas_result = [] # 图集数量超标图
    size_result = [] # 资源宽高超标图
    base_result.append(name)
    res_name = [] # 资源名称
    size = [] # 资源宽高
    filesize = [] # 资源文件大小
    # 记录超标资源
    oversize_res_name = []
    oversize_size = []
    oversize_filesize = []
    atlas_info = ui_data["atlas"]
    icon_info = ui_data["icon"]
    if len(atlas_info) > 0:
        res_name.append(ATLASIDENTIFIER)
        size.append("")
        filesize.append("")
        for key in atlas_info:
            # 跳过有问题的资源配置
            if len(atlas_info[key]) == 0:
                continue
            res_name.append(key)
            width, height, node = atlas_info[key]
            size.append("{} x {}".format(width, height))
            filesize.append(str(node))
            # 统计宽高超标资源
            if width > MAXUIRESOURCEWIDTH or height > MAXUIRESOURCEWIDTH:
                oversize_res_name.append(key)
                oversize_size.append("{} x {}".format(width, height))
                oversize_filesize.append(node)
        # 统计图集数量超标
        if len(atlas_info) > MAXATLASRESOURCE:
            atlas_result.append(name)
            atlas_result.append(BLOCKIDENTIFIER.join(res_name))
            atlas_result.append(BLOCKIDENTIFIER.join(size))
    if len(icon_info) > 0:
        res_name.append(ICONIDENTIFIER)
        size.append("")
        filesize.append("")
        for key in icon_info:
            # 跳过有问题的资源配置
            if len(icon_info[key]) == 0:
                continue
            res_name.append(key)
            width, height, node = icon_info[key]
            size.append("{} x {}".format(width, height))
            filesize.append(str(node))
            # 统计宽高超标资源
            if width > MAXUIRESOURCEWIDTH or height > MAXUIRESOURCEWIDTH:
                oversize_res_name.append(key)
                oversize_size.append("{} x {}".format(width, height))
                oversize_filesize.append(str(node))
    base_result.append(BLOCKIDENTIFIER.join(res_name))
    base_result.append(BLOCKIDENTIFIER.join(size))
    base_result.append(BLOCKIDENTIFIER.join(filesize))
    base_result.append(ui_data["count"])
    if len(oversize_res_name) > 0:
        size_result.append(name)
        size_result.append(BLOCKIDENTIFIER.join(oversize_res_name))
        size_result.append(BLOCKIDENTIFIER.join(oversize_size))
        size_result.append(BLOCKIDENTIFIER.join(oversize_filesize))
    return (base_result, atlas_result, size_result)

# 读取资源详细信息，长宽，文件大小
def readIconOrAtlasDetail(res_name, view_name) -> dict:
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
            print("File: {} not exist! Please check ui_setting of View: {}".format(res_path, view_name))
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
                        print("File: {} not exist! Please check atlas {}".format(png_path, res_path))
                        continue
        else:
            print("File: {} not exist! Please check ui_setting of View: {}".format(res_path, view_name))
            return result
    return result

# 整合传入的ui配置文件与现有的非公共资源配置，去除公共资源后输出
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
                    res_info = readIconOrAtlasDetail(res, view_name)
                    view_setting["icon"].update(res_info)
                    view_setting["count"] += 1
            else:
                if res not in view_setting["atlas"]:
                    res_info = readIconOrAtlasDetail(res, view_name)
                    view_setting["atlas"].update(res_info)
                    view_setting["count"] += len(res_info.keys())
    return nonpublic_uisetting

if __name__ == '__main__':
    ui_setting_path = os.path.join(UISETTINGPATHPREFIX, 'ui_setting.json')
    ui_setting_custom_path = os.path.join(UISETTINGPATHPREFIX, 'ui_setting_custom.json')
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
        print("File: {} is not accessible.".format(ui_setting_custom_path))
        exit(0)
    # 整合两个setting json，排除公共资源，输出一个面板所需的所有非公共资源
    nonpublic_uisetting = {}
    final_uisetting = outputNonpublicRes(ui_setting_custom, outputNonpublicRes(ui_setting, nonpublic_uisetting))
    

    # 制图报告
    base_data = []
    atlas_data = []
    size_data = []

    for key in final_uisetting:
        base, atlas, size = get_row_for_base(key, final_uisetting[key])
        base_data.append(base)
        if len(atlas):
            atlas_data.append(atlas)
        if len(size):
            size_data.append(size)
            
    base_data.sort(key=lambda x: (x[4]), reverse=True)

    tab = Tab(page_title="UI静态扫描报告")
    tab.add(table_base(base_data), "总览")
    if len(atlas_data):
        tab.add(table_atlas(atlas_data), "图集数量超标面板")
    if len(size_data):
        tab.add(table_size(size_data), "资源宽高超标面板")
    tab.render("ui_report.html")
    print("报告已生成...")
    os.system('pause')