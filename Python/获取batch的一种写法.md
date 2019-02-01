# 获取batch的一种写法

* [原代码](https://github.com/Determined22/zh-NER-TF/blob/81136cab7f9d318e7e9e7ef0961ef9f787fad1a8/data.py#L134), 当调用batc_yield函数时，使用时可以认为一次性获得了所有的batch,后面举出具体的例子
```python

def batch_yield(data, batch_size, vocab, tag2label, shuffle=False):
    """
    :param data:
    :param batch_size:
    :param vocab:
    :param tag2label:
    :param shuffle:
    :return:
    """
    if shuffle:
        random.shuffle(data)

    seqs, labels = [], []
    for (sent_, tag_) in data:
        sent_ = sentence2id(sent_, vocab)
        label_ = [tag2label[tag] for tag in tag_]

        if len(seqs) == batch_size:
            yield seqs, labels
            seqs, labels = [], []

        seqs.append(sent_)
        labels.append(label_)

    if len(seqs) != 0:
        yield seqs, labels

```

* 例子

```python

def batch_yield(data, batch_size):
    """
    :param data:
    :param batch_size:
    """
        if labels:
        data_labels = zip(data, labels)
        batch_data, batch_labels = [], []
        for (data_, label_) in data_labels:
            batch_data.append(data_)
            batch_labels.append(label_)

            if len(batch_data) == batch_size:
                yield batch_data, batch_labels
                batch_data, batch_labels = [], []

        if len(batch_data) != 0:
            yield batch_data, batch_labels

    else:
        batch_data = []
        for data_ in data:
            batch_data.append(data_)

            if len(batch_data) == batch_size:
                yield batch_data
                batch_data = []

        if len(batch_data) != 0:
            yield batch_data
    # seqs = []
    # for item in data:
    #
    #     if len(seqs) == batch_size:
    #         yield seqs
    #         seqs = []
    #     seqs.append(item)
    #
    # if len(seqs) != 0:
    #     yield seqs

if __name__ == '__main__':
    data = list(range(0,25))
    batch_size = 8
    batch = batch_yield(data, batch_size)

    for mini in batch:
        print (mini)

```

* 运行结果

[0, 1, 2, 3, 4, 5, 6, 7]

[8, 9, 10, 11, 12, 13, 14, 15]

[16, 17, 18, 19, 20, 21, 22, 23]

[24]


* 所以具体使用时，直接对Batch_yiedl进行遍历，每次拿到的是一个batch的全部内容
