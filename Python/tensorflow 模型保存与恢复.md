# tensorflow 模型保存与恢复1,2

## 一般的核心操作有如下

```python
import tensorflow as tf

"""保存"""
saver = tf.train.Saver(tf.global_variables())
# max_to_keep 参数用来设置保存模型的个数，默认为5，保存最近的5个模型。如果想每训练一代（epoch)就想保存一次模型，则可以将 max_to_keep设置为None或者0
# saver=tf.train.Saver(max_to_keep=0)

# 保存
# path设定保存的路径和名字，第三个参数将训练的次数作为后缀加入到模型名字中
saver.save(sess,path,global_step=step)

# 存储后，会生成四个文件：存储网络结构.meta、存储训练好的参数.data和.index、记录最新的模型checkpoint

"""模型恢复"""
# saver = tf.train.Saver()
# 使用tf.train.latest_checkpoint（）来自动获取最后一次保存的模型
# 这里要指出check_point的目录路径
model_file_path=tf.train.latest_checkpoint(checkpoint_path)
with tf.Session() as sess:
    saver.restore(sess, model_file_path)

```

# Tensorflow模型的保存与恢复2

根据[Tensorflow模型的保存与恢复](https://blog.csdn.net/irving_zhang/article/details/79081694)整理


## 保存

```python
# 创建saver
saver = tf.train.Saver(tf.all_variables())
# 保存模型
saver.save(sess,'save/model.ckpt',global_step=step)
# 或者 saver.save(sess,checkpoint_path,global_step=step)
"""
eg. saver.save(sess, 'my-model', global_step=0) ==>      filename: 'my-model-0'
"""

"""
在存储时，checkpoint_path中的最后一级目录，就是所存储checkmodel的前缀名，例如checkpoint_path="./save/checkpoint/model",
saver.save(sess, 'checkpoint_path, global_step=0)所得的filename为model-0

"""
```

## 恢复

```python

# 注意这里的checkpoint_path要与saver.save中的checkpoint_path一致  "./save/checkpoint/model"
model_file=tf.train.latest_checkpoint(checkpoint_path)
saver = tf.train.Saver()
saver.restore(sess,model_file)

```