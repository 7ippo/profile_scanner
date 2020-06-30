#encoding:utf-8

"""特效规格扫描

扫描特效资源，按照像素总大小降序排列

output:

{
    "effect1" : [ width, height, size],
    "effect2" : [ width, height, size],
    ...
}

authro: zpo

使用方法：
放在bin目录下

python effect_scanner.py

"""

import os
import re
from PIL import Image
from pyecharts.components import Table
from pyecharts import options as opts

EFFECTPATHPREFIX = "res/effect"

output = {}
# 只扫描png
effect_re = re.compile(r'\.png$')
for root, dirs, files in os.walk(EFFECTPATHPREFIX):
    for file in files:
        if effect_re.search(file):
            key = os.path.join(root, file)
            if os.path.exists(key):
                pic = Image.open(key)
                width, height = pic.size
                file_size = os.stat(key).st_size // 1024
                pixels_count = width * height
                name = root + "/" + file
                output[name] = [width , height, file_size, pixels_count]
            else:
                print("File: {} not exist! Please check effect res.".format(key))
                continue

# 最终绘制表格的数据
data = []
for key in output:
    name = re.sub(r'\\', '/', key)
    row = [ name ] + output[key]
    data.append(row)

data.sort(key=lambda x: (x[4]), reverse=True)

#  删掉像素统计，仅是用来排序不做展示
for i in range(len(data)):
    data[i].pop()

table = Table(page_title="特效资源规格扫描报告")
headers = ["特效路径", "宽", "高", "大小KB"]
table.add(headers, data)
table.set_global_opts(
    title_opts=opts.ComponentTitleOpts(title="特效资源规格扫描结果", subtitle="标准是1024x1024")
)
table.render("effect_report.html")
print("报告已生成...")
os.system('pause')