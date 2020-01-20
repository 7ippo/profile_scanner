#encoding:utf-8

"""数据展示和制图

authro: zpo

使用方法：
python graph_process.py [file]

options:
[file] 经过筛选输出的数据集ui_setting_nonpublic.json

"""

from pyecharts.components import Table
from pyecharts.charts import Tab
from pyecharts import options as opts

# 总览图
def table_base() -> Table:
    table = Table()

    headers = ["面板名称", "依赖资源", "宽 x 高", "大小(kb)", "网络请求数量"]
    rows = [
        ["AdventureRewardView", 
        '------icon------\nres/icon/equip_star_icon/success_bg2.png\nres/icon/equip_star_icon/attr_bg.png\nres/icon/equip_star_icon/success_bg720.png\nres/icon/equip_star_icon/success_bg1.png\n------atlas------\nadventure.png',
         '\n244 x 48\n409 x 106\n720 x 409\n196 x 54\n\n1024 x 1024',
         '\n18\n1\n118\n13\n\n597', 
         6]
    ]
    table.add(headers, rows).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="Table-我是主标题", subtitle="我是副标题支持换行哦")
    )
    return table

# 网络请求数量超标
# 依赖图集数量超标
# 图集宽高超标

tab = Tab(page_title="UI静态扫描报告")
tab.add(table_base(), "总览")
tab.render()
