#encoding:utf-8

"""数据展示和制图

authro: zpo

使用方法：
python graph_process.py [file]

options:
[file] 经过筛选输出的数据集ui_setting_nonpublic.json

"""
import json
import argparse
from pyecharts.components import Table
from pyecharts.charts import Tab
from pyecharts import options as opts

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

parser = argparse.ArgumentParser()
parser.add_argument('file', help='The path to ui_setting_nonpublic.json')

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

if __name__ == '__main__':
    args = parser.parse_args()
    if not(args.file):
        parser.print_help()
        exit(0)
    file_data = {}
    base_data = []
    atlas_data = []
    size_data = []
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
    except IOError:
        print("File: {} is not accessible.".format(args.file))
        exit(0)
    for key in file_data:
        base, atlas, size = get_row_for_base(key, file_data[key])
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
    tab.render()