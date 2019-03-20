# torch相关函数说明

## torch.squeeze()与torch.unsequeeze()

* https://blog.csdn.net/abc781cba/article/details/79663190

* https://blog.csdn.net/xiexu911/article/details/80820028

* torch.unsequeeze()   https://blog.csdn.net/flysky_jay/article/details/81607289


## torch.cat

* https://blog.csdn.net/qq_39709535/article/details/80803003

* https://blog.csdn.net/abc781cba/article/details/79663190

## torch.stack

* https://blog.csdn.net/Teeyohuang/article/details/80362756

* 注意Dim说明生成结果在哪个维度


## batch_norm

* https://blog.csdn.net/u014722627/article/details/68947016

* https://blog.csdn.net/u014532743/article/details/78456350

## nn与nn.function的区别

* [pytorch中 nn与nn.functional的区别](https://www.zhihu.com/question/66782101)

* 实际功能相同，但**nn.functional.xxx是函数接口，而nn.Xxx是nn.functional.xxx的类封装，并且nn.Xxx都继承于一个共同祖先nn.Module。这一点导致nn.Xxx除了具有nn.functional.xxx功能之外，内部附带了nn.Module相关的属性和方法，例如train(), eval(),load_state_dict, state_dict 等**

* nn.Xxx继承于nn.Module， 能够很好的与nn.Sequential结合使用， 而nn.functional.xxx无法与nn.Sequential结合使用。

* nn.Xxx不需要你自己定义和管理weight；而nn.functional.xxx需要你自己定义weight，每次调用的时候都需要手动传入weight, 不利于代码复用。

* PyTorch官方推荐：具有学习参数的（例如，conv2d, linear, batch_norm)采用nn.Xxx方式，没有学习参数的（例如，maxpool, loss func, activation func）等根据个人选择使用nn.functional.xxx或者nn.Xxx方式

## 数据读取

先按照(data,labels)的格式读取到torch.utils.data.Dataset()中，然后将DataSet传给DataLoader()??

* https://blog.csdn.net/geter_CS/article/details/83378786

* 初始应该是DataSet还是TensorDataset？什么区别？？ (几个例子好像都是用TensorDataset)

* [莫烦Python实例](https://morvanzhou.github.io/tutorials/machine-learning/torch/3-05-train-on-batch/)

* DataLoader中的collate_fn函数

    * 自定义一种取数据的方式

    * https://blog.csdn.net/weixin_42028364/article/details/81675021


## torch.bmm

* batch中的矩阵乘法

* https://blog.csdn.net/guotong1988/article/details/78707619


## torch.topk


* torch.topk(input, k, dim=None, largest=True, sorted=True, out=None) -> (Tensor, LongTensor)

    * 沿给定dim维度返回输入张量input中 k 个最大值。

    * 如果不指定dim，则默认为input的最后一维。
    
    * 如果为largest为 False ，则返回最小的 k 个值


## torch.transpose

* torch.transpose(input, dim0, dim1, out=None):

    * 返回输入矩阵input的转置，交换维度dim0和dim1。输入张量与输出张量共享内存。

    * input(Tensor) - 输入张量
    
    * dim0(int) - 转置的第一维
    
    * dim1(int) - 转置的第二维

## torch.save / torch.load

* https://morvanzhou.github.io/tutorials/machine-learning/torch/3-04-save-reload/

## pack_padded_sequence(input, lengths, batch_first=False)与pad_packed_sequence

### rnn.pack_padded_sequence

* 将一个 填充过的变长序列 压紧。（填充时候，会有冗余，所以压紧一下）

* 输入的形状可以是(T×B×* )。T是最长序列长度，B是batch size，*代表任意维度(可以是0)。如果batch_first=True的话，那么相应的 input size 就是 (B×T×*)。

* Variable中保存的序列，应该按序列长度的长短排序，长的在前，短的在后。即input[:,0]代表的是最长的序列，input[:, B-1]保存的是最短的序列。


* 参数说明:

   * input (Variable) – 变长序列 被填充后的 batch

   * lengths (list[int]) – Variable 中 每个序列的长度。

   * batch_first (bool, optional) – 如果是True，input的形状应该是B*T*size

### pad_packed_sequence(sequence, batch_first=False)

* 一下内容整理自: https://www.pytorchtutorial.com/docs/package_references/torch-nn/#torchnnutilsrnnpack_padded_sequenceinput-lengths-batch_firstfalsesource

* 上面提到的函数的功能是将一个填充后的变长序列压紧。 这个操作和pack_padded_sequence()是相反的。把压紧的序列再填充回来。

* 返回的Varaible的值的size是 T×B×\*, T 是最长序列的长度，B 是 batch_size,如果 batch_first=True,那么返回值是B×T×\*。

Batch中的元素将会以它们长度的逆序排列。

* 参数说明:

    * sequence (PackedSequence) – 将要被填充的 batch

    * batch_first (bool, optional) – 如果为True，返回的数据的格式为 B×T×\*。

    * 返回值: 一个tuple，包含被填充后的序列，和batch中序列的长度列表。

* 一篇更直观的文章: https://zhuanlan.zhihu.com/p/34418001


### torch自定义损失函数

* https://blog.csdn.net/yutingzhaomeng/article/details/80454545

* https://blog.csdn.net/yutingzhaomeng/article/details/80454807