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


* 阅读四: [tensorflow实现siamese网络-代码](https://blog.csdn.net/qq1483661204/article/details/79039702)

    * 核心操作在于：siamese函数定义网络(input1,input2都用这个网络计算) --->  input1,input2输入网络计算得到output1, output2 ---> seamese_loss计算损失

    * 损失函数步骤

        * 首先用l2范数定义output1和output2之间距离

        * 根据**output1和output2之间距离越小则损失函数值越小**，引入系数L<sub>g,L<sub>1，让L<sub>g满足单调递减,L<sub>1满足单调递增，满足距离和损失函数值间的关系;


        * 损失函数要满足的另外一个条件：**同类图片间距离必须比不同类之间的距离小**;此外还有**condition-2**和**condition-3**(见[文中](https://blog.csdn.net/qq1483661204/article/details/79039702)论文截图),得到**最终的损失函数表达式**。siamese_loss函数就是根据损失函数表达式进行计算(代码中的1-y和y是否写反了???)

    * 关于三重损失的疑问：如果input包括三类，分别是pos,neg,norm,一个正常样本(标注样本norm)，一个与标注样本norm同类的样本（正样本P），一个与标注数据不同类的样本（负样本N）。使标注样本A与正样本P的编码之间的距离小于等于A与负样本N的编码之间的距离，就是三重损失了？？？