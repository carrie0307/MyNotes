多gpu运行pytorch模型

### DataParallel()后，需要再加.cuda()

例如:

```python
model = torch.nn.DataParallel(BertForTokenClassification.from_pretrained('bert_model',
                                                                             num_labels=35,
                                                                             cache_dir='/data/event/models/bert-base-uncased'),
                                                                             device_ids = [0,1]).cuda()
```

所有要输model的数据，都再进行.cuda()操作 (将原来的所有to(device)操作换为.cuda())


### RNN使用DataParallel的注意事项

* 除了待输入的数据， 初始化h0和c0后，记得要.cuda()操作

* 不同batch会分配在不同gpu运行，运行后pad_packed_sequence函数会使得它们的max_len分别是各自batch下的batch_max_len,这样会导致不同gpu上的结果无法合并。因此需要设置pad_packed_sequence中的total_length参数为一个公共的MAX_LEN

```python

rnn_inputs = nn.utils.rnn.pack_padded_sequence(rnn_inputs, seq_lens, batch_first=True)
rnn_outputs, (ht, ct) = self.rnn(rnn_inputs, (h0, c0))
# 这里的total_length需要是每个batch统一的
rnn_outputs, _ = nn.utils.rnn.pad_packed_sequence(rnn_outputs, batch_first=True, total_length=max_len)

```


3.模型保存后加载的问题

* **尽可能在同一device上进行save与load,能避免很多麻烦**

* [官方文档](https://pytorch.org/tutorials/beginner/saving_loading_models.html#saving-torch-nn-dataparallel-models)给出的示例

* train及保存与load的device相同时，torch.load不需要map_location参数

* 如果模型保存和加载时的环境不同，例如使用GPU训练的模型保存后要在只有CPU的机器上运行,那么就需要使用参数map_location。

    * GPU ==> CPU 和 CPU ==> GPU 的map_location也可以直接写device, 例如```map_location=cpu```或```map_location=gpu:X```

```python


    # https://dingguanglei.com/pytorch-mo-xing-bao-cun-he-du-qu/

    # 把所有的张量加载到CPU中     GPU ==> CPU
    torch.load("network_path", map_location=lambda storage, loc: storage)
    # 把所有的张量加载到GPU 1中   
    torch.load("network_path", map_location=lambda storage, loc: storage.cuda(1))
    # 把张量从GPU 1 移动到 GPU 0
    torch.load("network_path", map_location={'cuda:1':'cuda:0'})
```

* 多卡训练并保存，单卡加载

* https://blog.csdn.net/jiangpeng59/article/details/79578266

```python
# 多卡的模型参数名中会多一个前缀"module."
kwargs={'map_location':lambda storage, loc: storage.cuda(gpu_id)}
def load_GPUS(model,model_path,kwargs):
    state_dict = torch.load(model_path,**kwargs)
    # create new OrderedDict that does not contain `module.`
    from collections import OrderedDict
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = k[7:] # remove `module.`
        new_state_dict[name] = v
    # load params
    model.load_state_dict(new_state_dict)
    return model

```

* 单GPU训练与保存，多GPU加载

自己测试后发现，将参数名添加上".module", map_location可以不写


* 多卡训练与保存，多卡加载

参数名应该不存在问题

如果device不同，那么map_location应该怎么设定呢??


* [此文](https://zhuanlan.zhihu.com/p/76604532)提供了```pythonmodel.module.state_dict()```的方法

    * [官方文档](https://pytorch.org/tutorials/beginner/saving_loading_models.html#saving-torch-nn-dataparallel-models)也给了这样的示例


### 关于map_location

map_location只在cpu、gpu发生迁移时使用?

