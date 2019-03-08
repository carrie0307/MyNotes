# torch数据获取示例

* 代码参考自 https://blog.csdn.net/weixin_42028364/article/details/81675021

```python
import torch
import torch.utils.data as data
import os
import pickle
import numpy as np


def collate_fn(data):
    
    # Sort a data list by caption length (descending order).
    items, labels, iitems = [], [], []
    for item,label in data:
        items.append(item + 100)
        labels.append(label)
        iitems.append('a')
    return items, labels, iitems

if __name__ == '__main__':
    test = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

    inputing = torch.tensor(np.array([test[i:i + 3] for i in range(10)]))
    target = torch.tensor(np.array([test[i:i + 1] for i in range(10)]))
    # print (inputing)
    # print (target)

    torch_dataset = data.TensorDataset(inputing, target)
    batch = 3

    loader = data.DataLoader(dataset=torch_dataset,batch_size=batch, collate_fn=collate_fn)
    # print ("=====================")
    for i in loader:
        print(i)


```