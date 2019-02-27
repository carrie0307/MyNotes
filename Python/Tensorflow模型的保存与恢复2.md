# Tensorflow模型的保存与恢复

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