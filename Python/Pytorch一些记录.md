# Pytorch一些记录

## 典型代码

* Pytorch-Transformer:Pytorch-Transformer: https://github.com/harvardnlp/annotated-transformer/blob/master/The%20Annotated%20Transformer.ipynb

* Pytorch典型NLP模型: https://github.com/AnubhavGupta3377/Text-Classification-Models-Pytorch

## 修改RNN激活函数

* [文档](https://pytorch.org/docs/stable/nn.html#torch.nn.RNNCell)

* 方法: 在初始化时加上**nonlinearity=relu**即可

## 卷积维度

* 如果F=h, padding=h//2(下取整),stride=1,则：

    * 若h为奇数,则输出w'=w(w,w'是卷积前后的维度)
    * 若h为偶数,则输出w'=w+1

## 对文本进行一维卷积

* 令**in_channels=word dim**,可以在max_len维度上(即同一个句子的不同词上)进行一维卷积(conv1d), 例如[C2ResRNN](https://tianchi.aliyun.com/forum/postDetail?spm=5176.12586969.1002.3.f21e4c2ajgjxNW&postId=48822)中的conv1d。(由于卷积前进行了transpose操作，所以最后一维维度为max_len,包含了每个时间步的信息)

## torch矩阵惩罚

* torch.mm 普通矩阵相乘

    * [文档与示例](https://pytorch.org/docs/stable/torch.html#torch.mm)

* torch.bmm batch下的矩阵相乘

    * [文档与示例](https://pytorch.org/docs/stable/torch.html#torch.bmm)


* torch.spmm???


## 关于batch_size

* 在模型model中尽量不要出现batch_size,因为batch划分可能存在最后一个batch不足batch_size的情况

* 即便手动划分训练时去掉了最后一个不满batch_size的batch,做test和inference时要注意保留下最后一个batch


## 随机数种子

```python
torch.manual_seed(args.seed) #为CPU设置种子用于生成随机数

if args.cuda: 
    torch.cuda.manual_seed(args.seed)#为当前GPU设置随机种子；如果使用多个GPU，应该使用torch.cuda.manual_seed_all()为所有的GPU设置种子。

```

* https://cloud.tencent.com/developer/article/114904

* https://cloud.tencent.com/developer/article/1149041

参见以上两文，设置如下代码对cudnn的卷积进行设置。

```python

# https://cloud.tencent.com/developer/article/114904
from torch.backends import cudnn
cudnn.benchmark = False            # if benchmark=True, deterministic will be False
cudnn.deterministic = True
```

## 参数

* named_parameters() 是给出网络层的名字和参数的迭代器
* parameters()会给出一个网络的全部参数的选代器

## masked_fill

* 文档https://pytorch-cn.readthedocs.io/zh/latest/package_references/Tensor/

masked_fill_(mask, value)
在mask值为1的位置处用value填充。mask的元素个数需和本tensor相同，但尺寸可以不同。

* 实例:https://blog.csdn.net/candy134834/article/details/84594754