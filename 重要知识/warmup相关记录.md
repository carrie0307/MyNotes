# 学习率 Warmup相关记录

## Warmup 原理

* 一篇记录: https://www.zhihu.com/question/338066667

* [Transformer中warm-up和LayerNorm的重要性探究](https://flashgene.com/archives/66828.html)

    * **Pre-LN Transformer，warm-up不再必要**

* [这里的transformer代码中包含了warm up的示例](https://nlp.seas.harvard.edu/2018/04/03/attention.html)

## warm up示例代码

```python

# From: https://zhuanlan.zhihu.com/p/50926409

# learning rate的warming up操作
def adjust_learning_rate(optimizer, gamma, epoch, step_index, iteration, epoch_size):
    """Sets the learning rate 
    # Adapted from PyTorch Imagenet example:
    # https://github.com/pytorch/examples/blob/master/imagenet/main.py
    """
    if epoch < args.warm_epoch:
        lr = 1e-6 + (args.lr-1e-6) * iteration / (epoch_size * args.warm_epoch)
    else:
        lr = args.lr * (gamma ** (step_index))

    for param_group in optimizer.param_groups:
        param_group['lr'] = lr

    return lr

```