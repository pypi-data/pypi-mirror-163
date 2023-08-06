
# 开发Knime节点

1、安装Knime分析平台，要求4.6.0以上版本
2、安装Knime Python扩展开发工具，它位于Knime Labs类别，可以从File->Install Knime Extensions ...中搜索Python。
3、下载base.zip，准备tutorial_extension扩展包，了解其中所包含的文件：
    - knime.yml: 定义Knime节点的基本信息的元数据；
    - my_extension.py: 定义Knime节点的功能的Python代码；
    - config.yml: 定义Knime节点的配置信息，包括对应的conda/python环境。
4、创建conda/python环境，并安装knime-python-base和knime-extension：
     conda install knime-python-base knime-extension -c knime -c conda-forge
5、编辑tutorial_extension目录外的config.yml文件，指定Knime节点的名称、源代码和conda环境等信息：
    <extension_id>:
        src: <path/to/folder/of/template>
        conda_env_path: <path/to/my_python_env>
        debug_mode: true
    其中，extension_id为knime.yml中指定的group_id和名字，例如org.tutorial.first_knime_node；
    src指定tutorial_extension文件夹的位置；
    conda_env_path指定之前创建的conda环境的位置，可以用conda env list查看；
    debug_mode指定是否开启调试模式，开启后，Knime节点会在节点运行时，输出调试信息，便于调试。
6、为了让Knime分析平台知道开发的节点config.yml所在位置，需要编辑Knime分析平台安装目录下的KNIME.ini文件，添加一行指定config.yml的路径：
    [KNIME.ini]
    -Dknime.python.extension.config=<path/to/config.yml>
7、运行Knime分析平台，在节点管理器中将会出现“My Template Node”节点。