# Pytorch-bn与dropout模型加载

## 问题描述

带有batch_normalization和dropout的模型，加载已训练好模型的参数pkl文件后，test的结果与原模型在训练时即时进行test的输出结果不同。

## 解决

具有bn和dropout的模型，加载参数后需要使用model.eval()固定bn和dp参数。


* [此文讲明了原因](https://blog.csdn.net/loseinvain/article/details/86476010)

* [此文讲明了操作](https://www.cnblogs.com/king-lps/p/8570021.html)