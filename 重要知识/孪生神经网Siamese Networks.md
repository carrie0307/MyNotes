# 孪生神经网Siamese Networks

* 阅读一: [孪生神经网](https://zhuanlan.zhihu.com/p/35040994)

    * 注意**孪生神经网**和**伪孪生神经网**


* 阅读二：[多种类型的孪生神经网络](https://www.cnblogs.com/Lee-yl/p/10113386.html) , 摘要如下

    * Siamese network就是“连体的神经网络”，神经网络的“连体”是通过**共享权值**来实现的

    * 孪生神经网络的用途：衡量两个输入的**相似程度**

    * 如果左右两边**不共享权值**，而是两个不同的神经网络，则模型叫pseudo-siamese network，伪孪生神经网络，如下图所示。对于pseudo-siamese network，**两边可以是不同的神经网络（如一个是lstm，一个是cnn）**，也可以是相同类型的神经网络。

    * 孪生神经网络用于处理两个输入**"比较类似"**的情况。伪孪生神经网络适用于处理两个输入**"有一定差别"**的情况。比如，我们要计算两个句子或者词汇的语义相似度，使用siamese network比较适合；如果验证标题与正文的描述是否一致（标题和正文长度差别很大），或者文字是否描述了一幅图片（一个是图片，一个是文字），就应该使用pseudo-siamese network。也就是说，要根据具体的应用，判断应该使用哪一种结构，哪一种Loss


    * 损失函数：传统的siamese network使用Contrastive Loss【对比损失函数】

    * 改进的Siamese网络（2-channel networks)

    * Triplet network： Siamese network是双胞胎连体，Triplet network是三胞胎连体；cost通过三重损失函数计算。


* 阅读三： paper[Deep metric learning using Triplet network](https://arxiv.org/abs/1412.6622)