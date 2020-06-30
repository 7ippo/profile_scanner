# ui_scanner使用方法

## 使用

effect_scanner_report.py用于扫描特效资源的规格，检查超标或异常的特效资源。
ui_scanner_report.py用于扫描UI配置并生成报告，检查不符合规格的UI资源。

如果因为pyecharts的问题导致无法打包成exe，使用方法见*开发*。

> 通过配置pyinstaller打包时拷贝资源解决了打包exe的问题，现在可以运行`pyinstaller -F ui_scanner_report.spec` 来打包exe了  
> 2020年6月30日 zpo

## 开发

如果目录结构有调整，可以修改脚本中`ATLASPATHPREFIX``UISETTINGPATHPREFIX`的值指明资源访问的相对路径，默认`ATLASPATHPREFIX="res/atlas"``UISETTINGPATHPREFIX="pre_load_config"`

~~~powershell
python effect_scanner_report.py
python ui_scanner_report.py
~~~

## 依赖开发环境

- 安装python
- pip install Pillow
- pip install pyecharts