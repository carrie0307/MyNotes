# tensorflow 模型保存与回复

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

# 使用tf.train.latest_checkpoint（）来自动获取最后一次保存的模型
# 这里要指出check_point的目录路径
model_file_path=tf.train.latest_checkpoint(checkpoint_path)
with tf.Session() as sess:
    saver.restore(sess, model_file_path)

```