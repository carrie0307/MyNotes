# dropout

* Deep learning调参经验

## dropout

### dropout添加在什么地方？


* 参考一:[Dropout一般加在什么地方?](https://blog.csdn.net/qq_27292549/article/details/81092653)

    * dropout应该添加在容易发生**过拟合**的地方，例如**全连接层**


* 参考二：[知乎:罗浩.ZJU](https://www.zhihu.com/question/41631631)

    * 分类问题用dropout, 只需要最后一层softmax前用基本就可以防止过拟合了，可能对accuracy提高不大，但是dropout前面的那层如果是之后要用的feature的话，性能就会大大提升。

### dropout设置为多少?

dropout_rate属于超参数，一般输入层dropout比较少，dropout rate是0.1或0; 中间层可以稍大，例如0.5；一般0.5较为常用。

* [dropout rate一般设置多大](http://sofasofa.io/forum_main_post.php?postid=1001988)

## learning_rate

* 参考二：[知乎:罗浩.ZJU](https://www.zhihu.com/question/41631631)

随着网络训练的进行，学习率要逐渐降下来，如果有tensorboard可能会发现在学习率下降的一瞬间网络会有巨大的性能提升。同样fine-tuning也要格局模型性能设置合适的学习率，比如一个已训练好的模型如果使用较大的学习率，那么之前可能就白训练了，也就是说,**网络性能越好，学习率越要小**。


### 怎么减小learning rate？

#### 一下内容整理自[Pytorch调整学习率的六种方法](https://blog.csdn.net/shanglianlm/article/details/85143614)

```python
torch.optim.lr_scheduler.StepLR(optimizer, step_size, gamma=0.1, last_epoch=-1)

# step_size(int)- 学习率下降间隔数，若为 30，则会在 30、 60、 90…个 step 时，将学习率调整为 lr*gamma。
# gamma(float)- 学习率调整倍数，默认为 0.1 倍，即下降 10 倍。
# last_epoch(int)- 上一个 epoch 数，这个变量用来指示学习率是否需要调整。当last_epoch 符合设定的间隔时，就会对学习率进行调整。当为-1 时，学习率设置为初始值。
```

* 按需调整学习率 MultiStepLR

按设定的间隔调整学习率，这个方法适合后期调试使用，观察loss曲线，为每个实验定制调整时机

```python
torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones, gamma=0.1, last_epoch=-1)

# milestones(list)- 一个 list，每一个元素代表何时调整学习率， list 元素必须是递增的。如 milestones=[30,80,120]
# gamma(float)- 学习率调整倍数，默认为 0.1 倍，即下降 10 倍。
```

* 指数衰减调整学习率

按照指数筛检调整学习率，公式:lr = lr * gamma ** epoch

```python
torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma, last_epoch=-1)

# gamma- 学习率调整倍数的底，指数为 epoch，即 gamma**epoch
```

* 余弦退火调整学习率CosineAnnealingLR

以余弦函数为周期，并在每个周期最大值时重新设置学习率。以初始学习率为最大学习率，以 2×Tmax 2×Tmax2×Tmax 为周期，在一个周期内先下降，后上

```python
torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max, eta_min=0, last_epoch=-1)

# T_max(int)- 一次学习率周期的迭代次数，即 T_max 个 epoch 之后重新设置学习率。
# eta_min(float)- 最小学习率，即在一个周期中，学习率最小会下降到 eta_min，默认值为 0。
```

* 自适应调整学习率ReduceLROnPlateau

当某指标不再变化（下降或升高），调整学习率，这是非常实用的学习率调整策略。例如，当验证集的 loss 不再下降时，进行学习率调整；或者监测验证集的 accuracy，当accuracy 不再上升时，则调整学习率

    * reduceLROnPlateau一个实例:http://www.spytensor.com/index.php/archives/32/?dmpmjm=1aivz (optimizer.step())

```python
torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=10, verbose=False, threshold=0.0001, threshold_mode='rel', cooldown=0, min_lr=0, eps=1e-08)

# mode(str)- 模式选择，有 min 和 max 两种模式， min 表示当指标不再降低(如监测loss)， max 表示当指标不再升高(如监测 accuracy)。
# factor(float)- 学习率调整倍数(等同于其它方法的 gamma)，即学习率更新为 lr = lr * factor
# patience(int)- 忍受该指标多少个 step 不变化，当忍无可忍时，调整学习率。
# verbose(bool)- 是否打印学习率信息， print(‘Epoch {:5d}: reducing learning rate of group {} to {:.4e}.’.format(epoch, i, new_lr))
# threshold_mode(str)- 选择判断指标是否达最优的模式，有两种模式， rel 和 abs。
# 当 threshold_mode == rel，并且 mode == max 时， dynamic_threshold = best * ( 1 +threshold )；
# 当 threshold_mode == rel，并且 mode == min 时， dynamic_threshold = best * ( 1 -threshold )；
# 当 threshold_mode == abs，并且 mode== max 时， dynamic_threshold = best + threshold ；
# 当 threshold_mode == rel，并且 mode == max 时， dynamic_threshold = best - threshold；
# threshold(float)- 配合 threshold_mode 使用。
# cooldown(int)- “冷却时间“，当调整学习率之后，让学习率调整策略冷静一下，让模型再训练一段时间，再重启监测模式。
# min_lr(float or list)- 学习率下限，可为 float，或者 list，当有多个参数组时，可用 list 进行设置。
# eps(float)- 学习率衰减的最小值，当学习率变化小于 eps 时，则不调整学习率
```

* 自定义调整学习率 LambdaLR

为不同参数组设定不同学习率调整策略。调整规则为，

```
lr=base_lr×lmbda(self.last_epoch) lr = base\_lr ×lmbda(self.last\_epoch)
lr=base_lr×lmbda(self.last_epoch)
```

fine-tune 中十分有用，我们不仅可为不同的层设定不同的学习率，还可以为其设定不同的学习率调整策略。

```python
torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda, last_epoch=-1)

# lr_lambda(function or list)- 一个计算学习率调整倍数的函数，输入通常为 step，当有多个参数组时，设为 list。
```

* 使用注意事项

    * https://github.com/ClementPinard/SfmLearner-Pytorch/issues/5
    
    * https://github.com/pytorch/pytorch/issues/3814

    * scheduler.step() 每个epoch后 (scheduler.step()只是修改学习率,训练优化过程还是需要optimizer的一般常规操作进行);
optimizer.step() 每个mini_batch后

## 梯度裁剪 clip

### [浅谈神经网络中的梯度爆炸问题](https://zhuanlan.zhihu.com/p/32154263)

    * 梯度爆炸会引发哪些问题: 导致网络不稳定，无法从训练数据中进行正常学习

    * 怎么知道**是否出现了梯度爆炸？**

        * 模型无法在训练数据上收敛(比如，损失函数值非常差)

        * 模型不稳定(在更新的时候损失有较大的变化)

        * 模型的损失函数值在训练过程中变为NaN

    * 不太明显的判断梯度爆炸的方法:

        * 模型在训练过程中，**权重变化非常大**

        * 模型训练过程中，**权重变成NaN值**

        * 每层的每个节点在训练时，其误差梯度一直是大于1.0

    * 解决方法

        * 修正网络结构

        * 使用Relu做激活函数

        * 梯度裁剪

### [理解梯度下降](http://liuchengxu.org/blog-cn/posts/dive-into-gradient-decent/)

* 梯度的**范数**：某一点处的方向导数在其梯度方向上达到**最大值，此最大值即梯度的范数**

* [警惕!Loss为Nan或超级大的原因](https://oldpan.me/archives/careful-train-loss-nan-inf)

* [梯度裁剪及其作用](https://wulc.me/2018/05/01/%E6%A2%AF%E5%BA%A6%E8%A3%81%E5%89%AA%E5%8F%8A%E5%85%B6%E4%BD%9C%E7%94%A8/)

### Pytorch 梯度裁剪

* [Pytorch梯度裁剪](https://www.cnblogs.com/lindaxin/p/7998196.html)

* [神经网络调参细节](https://yq.aliyun.com/articles/610082/)

```python
for batch in text_batch_list:

    model.train()

    optimizer.zero_grad()
    """
    其他常规操作
    """
    if self.clip_grad:
        torch.nn.utils.clip_grad_norm(model.parameters, 10)

    

```

梯度裁剪用于解决**梯度爆炸**问题,具体操作是**限制最大梯度，如果梯度达到最大阈值则让它根据衰减系数衰减**。



Pytorch中梯度裁剪通过clip_grad进行,函数文档[clip_grad_norm](https://pytorch.org/docs/stable/_modules/torch/nn/utils/clip_grad.html),其中参数[含义](https://www.cnblogs.com/lindaxin/p/7998196.html)为:

```
parameters (Iterable[Variable]) – 一个基于变量的迭代器，会进行归一化（原文：an iterable of Variables that will have gradients normalized）

max_norm (float or int) – 梯度的最大范数（原文：max norm of the gradients）

norm_type(float or int) – 规定范数的类型，默认为L2（原文：type of the used p-norm. Can be'inf'for infinity norm）

Returns:参数的总体范数（作为单个向量来看）（原文：Total norm of the parameters (viewed as a single vector).）
```

```python

optimizer.zero_grad()        
loss, hidden = model(data, hidden, targets)
loss.backward()
# clip应该是多少???
torch.nn.utils.clip_grad_norm(model.parameters(), clip)
optimizer.step()
```


## 初始化

* 初始化非常重要，参数的初始化会影响**是否能够收敛**以及**收敛的速度**

* [torch.nn.init - source code](https://pytorch.org/docs/stable/_modules/torch/nn/init.html)

* [torch.nn.init - doc](https://pytorch.org/docs/stable/nn.html#torch-nn-init)


* [知乎:萧瑟](https://www.zhihu.com/question/41631631/answer/94816420)

    * uniform均匀分布初始化：
    
```
w = np.random.uniform(low=-scale, high=scale, size=[n_in,n_out])
Xavier初始法，适用于普通激活函数(tanh,sigmoid)：scale = np.sqrt(3/n)He初始化，适用于ReLU：scale = np.sqrt(6/n)normal高斯分布初始化：
```
    * normal正态分布初始化

```
w = np.random.randn(n_in,n_out) * stdev # stdev为高斯分布的标准差，均值设为0
Xavier初始法，适用于普通激活函数 (tanh,sigmoid)：stdev = np.sqrt(n)He初始化，适用于ReLU：stdev = np.sqrt(2/n)
```

* [一个样例初始化函数](https://github.com/ShomyLiu/pytorch-pcnn/blob/e1c95ed6bef369f08550043f79779f1d301dd236/models/PCNN.py#L42)

```python

def init_model_weight(self):
        '''
        use xavier to init
        '''
        # nn.init.xavier_normal_(self.cnn_linear.weight)
        # nn.init.constant_(self.cnn_linear.bias, 0.)
        nn.init.xavier_normal_(self.out_linear.weight)
        nn.init.constant_(self.out_linear.bias, 0.)
        # for conv in self.convs:
        #     nn.init.xavier_normal_(conv.weight)
        #     nn.init.constant_(conv.bias, 0)

```

* 使用nn.Parameter()的初始化

* nn.Parameter()可以直接给权重矩阵进行特殊的初始化，例如

```python
self.out_linear.weight = torch.nn.Parameter(torch.ones(in_dim, out_dim))
self.out_linear.bias = torch.nn.Parameter(torch.ones(out_dim))
```

* 在Attention中使用nn.Parameter()初始化

    * 例1: https://www.jianshu.com/p/d8b77cc02410

    * 例2： https://pytorch.org/tutorials/beginner/chatbot_tutorial.html
    ```python
    self.v = nn.Parameter(torch.FloatTensor(hidden_size))
    ```
* nn.Parameter()默认**requires_grad=True**,见[中文文档](https://pytorch-cn.readthedocs.io/zh/latest/package_references/torch-nn/)

## Batch_norm (归一化/标准化)

### [深度学习中Batch Normalization为什么效果好](https://www.zhihu.com/question/38102762)

* [BatchNorm原理解释](https://www.cnblogs.com/guoyaohua/p/8724433.html)

* BN的好处 - [知乎:龙鹏-言有三](https://www.zhihu.com/question/38102762/answer/607815171)

    * 减轻了对**参数初始化的依赖**，这是**利于调参**

    * **训练更快**，可以使用更高的学习率。

    * BN一定程度上增加了**泛化能力，dropout等技术可以去掉**

* BN的缺陷 - [知乎:龙鹏-言有三](https://www.zhihu.com/question/38102762/answer/607815171)

batch normalization依赖于batch的大小，**当batch值很小时，计算的均值和方差不稳定**。研究表明对于ResNet类模型在ImageNet数据集上，batch从16降低到8时开始有非常明显的性能下降，在训练过程中计算的均值和方差不准确，而在测试的时候使用的就是训练过程中保持下来的均值和方差。这一个特性，导致batch normalization不适合以下的几种场景:

    * batch非常小，比如训练资源有限无法应用较大的batch，也比如在线学习等使用单例进行模型参数更新的场景。

    * rnn，因为它是一个动态的网络结构，同一个batch中训练实例有长有短，导致每一个时间步长必须维持各自的统计量，这使得BN并不能正确的使用。在rnn中，对bn进行改进也非常的困难。不过，困难并不意味着没人做，事实上现在仍然可以使用的，不过这超出了咱们初识境的学习范围


* 什么时候使用Batch_norm？

例如，在神经网络训练时遇到收敛速度很慢，或梯度爆炸等无法训练的状况时可以尝试BN来解决。另外，在一般使用情况下也可以加入BN来加快训练速度，提高模型精度

### pytorch中Batch_norm

* batchnorm1d和batchnorm2d什么区别???

    * torch.nn.BatchNorm1d(num_features): Applies Batch Normalization over a 2D or 3D input 
    * num_features： 来自期望输入的特征数，该期望输入的大小为'batch_size x num_features [x width]'
    * 输入：（N, C）或者(N, C, L)
    * 输出：（N, C）或者（N，C，L） (输入输出相同,C就相当于num_features)


    *  torch.nn.BatchNorm2d(num_features): Applies Batch Normalization over a 4D input
    * num_features： 来自期望输入的特征数，该期望输入的大小为'batch_size x num_features x height x width
    * 输入：（N, C，H, W) - 输出：（N, C, H, W）(输入输出相同,C就相当于num_features)

### 什么位置添加BN

* [CNN RNN哪里添加BN](https://blog.csdn.net/malefactor/article/details/51549771)

    * RNN可以考虑横向或纵向，横向没有细致研究，纵向可以尝试在最后的线性输出前添加batch_norm。

    * CNN是在卷积后? 卷积后一个feature map的结果就相当于一个神经元，将输出feature_map数量作为num_features进行bn (https://blog.csdn.net/hjimce/article/details/50866313)


## 动量

* 参考1:https://blog.csdn.net/u013989576/article/details/70241121

* 参考2：https://www.jqr.com/article/000505

动量法不仅使用当前的梯度，同时还利用之前的梯度提供的信息

* 参考3: https://zh.gluon.ai/chapter_optimization/momentum.html

当动量参数(momentum factor)γ=0s时,**动量法等价于小批量随机梯度下降**。


## 优化函数

### [深度学习最全优化方法总结比较]

weight_decay是类似L2的实现

#### SGD

```python
torch.optim.SGD(params, lr=<required parameter>, momentum=0, dampening=0, weight_decay=0, nesterov=False)
```

* 普通的随机梯度下降

* 缺点

    * **learning_rate的选择较为困难**

    * 容易收敛到**局部最优**，某些情况下可能被困在**鞍点**

    * 因此引入了**动量**,动量法不仅使用当前的梯度，同时还利用之前的梯度提供的信息

#### AdaGrad

```python
torch.optim.Adagrad(params, lr=0.01, lr_decay=0, weight_decay=0, initial_accumulator_value=0)
```

* AdaGrad是对学习率进行了**约束**


#### Adadelta

```python
torch.optim.Adadelta(params, lr=1.0, rho=0.9, eps=1e-06, weight_decay=0)
```
Adadelta是对Adagrad的拓展，仍然是对学习率的自适应约束，但是计算上进行了简化。


#### RMSprop

```python
torch.optim.RMSprop(params, lr=0.01, alpha=0.99, eps=1e-08, weight_decay=0, momentum=0, centered=False)
```

RMSprop可以看作Adadelta的一个特例

#### Adam

```python
torch.optim.Adam(params, lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0, amsgrad=False)
```

Adam本质上是带有动量项的RMSprop


## 正则化

* [Pytorch中的L2和L1正则化](https://blog.csdn.net/LoseInVain/article/details/81708474)

在pytorch中，通过torch.optim.optimizer的weight_decay参数实现L2，但这会对所有参数都进行L2惩罚。

如果要实现L1, 则需要另外写代码。

## 其他阅读

* [A Recipe for Training Neural Netowrks](https://karpathy.github.io/2019/04/25/recipe/)

* [神经网络调参细节](https://yq.aliyun.com/articles/610082/)

* [深度网络调参技巧](https://zhuanlan.zhihu.com/p/24720954)
