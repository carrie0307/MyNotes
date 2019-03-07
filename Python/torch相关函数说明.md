# torch相关函数说明

## torch.squeeze()与torch.unsequeeze()

* https://blog.csdn.net/abc781cba/article/details/79663190

* https://blog.csdn.net/xiexu911/article/details/80820028

* torch.unsequeeze()   https://blog.csdn.net/flysky_jay/article/details/81607289


## torch.cat

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

    * https://blog.csdn.net/u012436149/article/details/78545766