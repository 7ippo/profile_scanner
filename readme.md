# ui_scanner使用方法

## 使用

把脚本放置在bin目录下，双击。

## 开发

如果目录结构有调整，可以修改脚本中`ATLASPATHPREFIX``UISETTINGPATHPREFIX`的值指明资源访问的相对路径，默认`ATLASPATHPREFIX="res/atlas"``UISETTINGPATHPREFIX="pre_load_config"`

~~~powershell
python ui_scanner.py
~~~

## 依赖开发环境

- 安装python
- pip install Pillow
