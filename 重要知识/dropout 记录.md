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

* 问题:torch.optim.lr_scheduler需要用zero_grad吗? scheduler.step()是不是要放在train函数前面?

* 等间隔调整学习率StepLR
last_epoch什么意思???

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

限制最大梯度，如果梯度达到最大阈值则让它根据衰减系数衰减。

## 优化函数

## 初始化


uniform均匀分布初始化：
w = np.random.uniform(low=-scale, high=scale, size=[n_in,n_out])
Xavier初始法，适用于普通激活函数(tanh,sigmoid)：scale = np.sqrt(3/n)He初始化，适用于ReLU：scale = np.sqrt(6/n)normal高斯分布初始化：
w = np.random.randn(n_in,n_out) * stdev # stdev为高斯分布的标准差，均值设为0
Xavier初始法，适用于普通激活函数 (tanh,sigmoid)：stdev = np.sqrt(n)He初始化，适用于ReLU：stdev = np.sqrt(2/n)

uniform和normal初始化的xavier初始化不同嘛???
以上初始化部分内容摘自[知乎:萧瑟](https://www.zhihu.com/question/41631631/answer/94816420)


## 归一化

## 其他阅读

* [A Recipe for Training Neural Netowrks](https://karpathy.github.io/2019/04/25/recipe/)

