# nn.ModuleList与nn.Sequential

* [When should I use nn.ModuleList and when should I use nn.Sequential](https://discuss.pytorch.org/t/when-should-i-use-nn-modulelist-and-when-should-i-use-nn-sequential/5463/10)

    * nn.ModuleList does not have a forward() method, because it does not define any neural network, that is, there is **no connection** between each of the nn.Module's that it stores

* [Pytorch中nn.ModuleList和nn.Sequential](https://blog.csdn.net/xiaojiajia007/article/details/82118559)

### 总结

* 将x输入nn.Sequential后,x会被Sequential中的每个模型依次处理，最终的输出是Sequential中所有模型处理后的结果;

* nn.ModuleList只是模型的列表，如下的调用方法得到的x也是一个列表，是分别被self.convs中子模型所处理后的输出结果。

```python
self.convs = nn.ModuleList([nn.Conv2d(1, self.opt.filters_num, (k, feature_dim), padding=(int(k / 2), 0)) for k in self.opt.filters])
x = [F.relu(conv(x)).squeeze(3) for conv in self.convs]
```