Orange3-FinEcon
======================

Note: 日期数据转换有问题，为pandas一个缺陷，tzlocal=2.1可以解决此问题。

在Orange3中整合其它功能的自己开发的包。

ln -s /Applications/Orange3.app/Contents/MacOS/pip /usr/local/bin/pip
ln -s /Applications/Orange3.app/Contents/MacOS/python /usr/local/bin/python
ln -s /Applications/Orange3.app/Contents/MacOS/python /usr/local/bin/python3

## 安装

/Applications/Orange3.app/Contents/MacOS/pip install -e /Users/rayhe/PycharmProjects/orange3-FinEcon

## 安装的其它第三方包：

因果分析：

pip install orange3-associate  orange3-explain orange3-educational orange3-text orange3-timeseries~~

pip install -U diffeqpy  linearmodels arch econml
pip install -U evalml "featuretools[tsfresh]" rpy2

#R_HOME  设置有问题。

py-mint


auto-sklearn 好像安装不了，
pycaret因为版本的原因，pycaret 2.3.5肯定是安装不了。


This is an example add-on for [Orange3](http://orange.biolab.si). Add-on can extend Orange either 
in scripting or GUI part, or in both. We here focus on the GUI part and implement a simple (empty) widget,
register it with Orange and add a new workflow with this widget to example tutorials.

Installation
------------

To install the add-on from source run

    pip install .

To register this add-on with Orange, but keep the code in the development directory (do not copy it to 
Python's site-packages directory), run

    pip install -e .

Documentation / widget help can be built by running

    make html htmlhelp

from the doc directory.

Usage
-----

After the installation, the widget from this add-on is registered with Orange. To run Orange from the terminal,
use

    orange-canvas

or

    python -m Orange.canvas

The new widget appears in the toolbox bar under the section Example.

![screenshot](https://github.com/biolab/orange3-example-addon/blob/master/screenshot.png)


##  Orchest
##### 密码12）
docker container prune
docker image prune -a
git clone https://github.com/orchest/orchest.git && cd orchest
./orchest install --lang=all
./orchest start

### Orchest设置

###### 环境镜像
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes

#!/bin/bash
pip config set global.index-url https://pypi.doubanio.com/simple
sudo apt-get install -y graphviz
pip install -U --no-cache-dir jupyterlab streamlit
pip install -U --no-cache-dir matplotlib SciencePlots chineseize-matplotlib seaborn
pip install -U --no-cache-dir causalml[tf] econml
pip install -U --no-cache-dir evalml --ignore-installed pyyaml
pip install -U --no-cache-dir pandas-profiling sweetviz autoviz
pip install -U --no-cache-dir lux-api dice-ml
pip install --no-cache-dir mitosheet3
pip install -U --no-cache-dir pyqlib panel
pip install -U --no-cache-dir transformers

###### JupyterLab配置镜像
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
git config --global user.name "haharay"
git config --global user.email "hcmray@qq.com"
pip install jupyterlab-drawio
pip install mitosheet3
jupyter lab build --minimize=False
jupyter labextension list


###### 其它配置镜像
金融数据分析：坚持写下去。