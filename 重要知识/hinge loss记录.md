# Hinge_loss记录

## Hinge Loss 变种

* 以下内容整理自[理解Hinge Loss](https://blog.csdn.net/fendegao/article/details/79968994)

* 下文直接讨论变种HingeLoss的部分

```
L(y,y') = max(0, margin-(y-y'))
        = max(0, margin+(y'-y))
        = max(0, margin+y'-y)
```

其中，y是正确预测的分数，y'是错误预测的分数，二者差值可以用来表示某种**相似关系**,margin是可以自由设置的系数。此目标函数的目的是:**让y的分数高于y',且高出一个margin即可**(如果高出的部分超过margin,差距加大不会有任务奖励)

## 三重损失函数

看到Hinge Loss后想到[三重损失](https://www.cnblogs.com/Lee-yl/p/10113386.html)，再次进行记录。

* 公式:L(A,P,N)= max(0, margin+|f(A)-f(P)|<sup>2</sup>+|f(A)-f(N)|<sup>2</sup>)


* 式中，|f(A)-f(P)|<sup>2</sup>表示与A同类样本与A的距离，|f(A)-f(N)|<sup>2</sup>表示与A异类样本与A的距离，函数的目的是:**让与A异类样本与A的距离比与A同类样本与A的距离大margin**


## 问题:

虽然Hinge Loss式中有一个max,但最终目的还是要使Hinge Loss最小???