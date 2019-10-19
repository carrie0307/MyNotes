# Pointer Network & MATCH-LSTM

## Pointer Network

* 一篇讲解: https://lianhaimiao.github.io/2018/08/21/Pointer-Network-%E7%9A%84%E4%B8%80%E4%BA%9B%E7%90%86%E8%A7%A3/

* 个人理解: 利用atten机制计算attn weights, 但不是用权重去进行加权和运算，而是将attn权重作为关于input sequence中每个token的概率分布，选择概率最大(即attn权重)的token作为选中的token.

* [Pointer Network的作用](https://lianhaimiao.github.io/2018/08/21/Pointer-Network-%E7%9A%84%E4%B8%80%E4%BA%9B%E7%90%86%E8%A7%A3/)

    * 提供了一种新视角去理解 Attention，把 Attention 作为一种求分布的手段(可以直接从输入序列生成输出序列)。

    * 对于输出字典长度不固定问题提供了一种新的解决方案。

    * 将输入作为输出的一种补充手段，让输出部分可以更好的引入输入部分的信息


* [Pointer Networks and copy mechanism](https://panxiaoxie.cn/2018/08/25/%E8%AE%BA%E6%96%87%E7%AC%94%E8%AE%B0-Pointer-Networks/)

## Match LSTM

整理相关讲解文章如下:

* https://blog.csdn.net/tiweeny/article/details/81437763

* https://blog.csdn.net/chazhongxinbitc/article/details/78724911

* https://panxiaoxie.cn/2018/08/14/%E8%AE%BA%E6%96%87%E7%AC%94%E8%AE%B0-Match-LSTM/