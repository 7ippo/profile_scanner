# ui_scanner使用方法

## 使用

ui_scanner.exe用于简单扫描UI配置，将其放置在bin目录下，双击使用。
ui_scanner_report.py用于扫描UI配置并生成报告，检查不符合规格的UI资源，因为pyecharts的问题导致无法打包成exe，使用方法见*开发*。

## 开发

如果目录结构有调整，可以修改脚本中`ATLASPATHPREFIX``UISETTINGPATHPREFIX`的值指明资源访问的相对路径，默认`ATLASPATHPREFIX="res/atlas"``UISETTINGPATHPREFIX="pre_load_config"`

~~~powershell
python ui_scanner.py
python ui_scanner_report.py
~~~

## 依赖开发环境

- 安装python
- pip install Pillow
- pip install pyecharts