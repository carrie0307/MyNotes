# Pytorch可视化

## visdom

* 基础: https://zhuanlan.zhihu.com/p/34692106

    * 安装建议从github下载后 python setup.py install

* 使用

    * 运行"python -m visdom.server"(第一次运行会下载相关js文件，注意观察命令行输出的提示信息)

    * 平时使用时，先"python -m visdom.server"运行,然后运行相关的visdom文件


## graphivx

* https://github.com/szagoruyko/pytorchviz

* 关于参数

    * named_parameters() 是给出网络层的名字和参数的迭代器
    * parameters()会给出一个网络的全部参数的选代器