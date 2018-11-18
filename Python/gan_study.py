import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
from tensorflow.examples.tutorials.mnist import input_data
# 本文代码转载自：https://blog.csdn.net/u012223913/article/details/75051516
# https://wiseodd.github.io/techblog/2016/09/17/gan-tensorflow/
# 另外一个参考资料：https://www.jianshu.com/p/08abd788d598
# 代码可直接运行

"""
1. 为什么generator输出定位784维最后直接就能得到图形，discriminator输出定为1最后得到就是概率？ 两个计算表达式都是一样的
2. 原文中说只能mininize(优化时只能用mininize函数)，所以加上了负号表示最大值？
3. 这是最基础的GAN,具体使用还有哪些可以修改提升？？
4. 注意feedback函数，将待计算变量运算关系中所有涉及到的只有placehold的变量带入
"""

sess = tf.InteractiveSession()

mb_size = 128
Z_dim = 100

mnist = input_data.read_data_sets('../../MNIST_data', one_hot=True)

# 声明变量
def weight_var(shape, name):
    return tf.get_variable(name=name, shape=shape, initializer=tf.contrib.layers.xavier_initializer())


def bias_var(shape, name):
    return tf.get_variable(name=name, shape=shape, initializer=tf.constant_initializer(0))


# discriminater net
X = tf.placeholder(tf.float32, shape=[None, 784], name='X')
D_W1 = weight_var([784, 128], 'D_W1')
D_b1 = bias_var([128], 'D_b1')
D_W2 = weight_var([128, 1], 'D_W2')
D_b2 = bias_var([1], 'D_b2')
theta_D = [D_W1, D_W2, D_b1, D_b2]


# generator net
Z = tf.placeholder(tf.float32, shape=[None, 100], name='Z')
# 为什么接收是100维？
G_W1 = weight_var([100, 128], 'G_W1')
G_b1 = bias_var([128], 'G_B1')
G_W2 = weight_var([128, 784], 'G_W2')
G_b2 = bias_var([784], 'G_B2')
theta_G = [G_W1, G_W2, G_b1, G_b2]

"""
为什么generator输出定位784维最后直接就能得到图形，discriminator输出定为1最后得到就是概率？ 两个计算表达式都是一样的
"""
# 定义模型
def generator(z):
    G_h1 = tf.nn.relu(tf.matmul(z, G_W1) + G_b1)
    G_log_prob = tf.matmul(G_h1, G_W2) + G_b2
    G_prob = tf.nn.sigmoid(G_log_prob)
    return G_prob

def discriminator(x):
    D_h1 = tf.nn.relu(tf.matmul(x, D_W1) + D_b1)
    D_logit = tf.matmul(D_h1, D_W2) + D_b2
    D_prob = tf.nn.sigmoid(D_logit)
    return D_prob, D_logit

G_sample = generator(Z)
D_real, D_logit_real = discriminator(X)
# 判别器对生成器生成的样本进行判别的结果
D_fake, D_logit_fake = discriminator(G_sample)

# 由于tensorflow只能做minimize，loss function可以写成如下：
D_loss = -tf.reduce_mean(tf.log(D_real) + tf.log(1. - D_fake))
G_loss = -tf.reduce_mean(tf.log(D_fake))
# 优化
D_optimizer = tf.train.AdamOptimizer().minimize(D_loss, var_list=theta_D)
G_optimizer = tf.train.AdamOptimizer().minimize(G_loss, var_list=theta_G)

# 训练 & 保存生成的图谱
def sample_Z(m, n):
    '''Uniform prior for G(Z)'''
    return np.random.uniform(-1., 1., size=[m, n])

def plot(samples):
    fig = plt.figure(figsize=(4, 4))
    gs = gridspec.GridSpec(4, 4)
    gs.update(wspace=0.05, hspace=0.05)

    for i, sample in enumerate(samples):  # [i,samples[i]] imax=16
        ax = plt.subplot(gs[i])
        plt.axis('off')
        ax.set_xticklabels([])
        ax.set_aspect('equal')
        plt.imshow(sample.reshape(28, 28), cmap='Greys_r')

    return fig


if not os.path.exists('out/'):
    os.makedirs('out/')

sess.run(tf.global_variables_initializer())

i = 0
for it in range(1000000):
    if it % 1000 == 0:
        # 用生成器生成数据
        samples = sess.run(G_sample, feed_dict={
                           Z: sample_Z(16, Z_dim)})  # 16*784
        fig = plot(samples)
        plt.savefig('out/{}.png'.format(str(i).zfill(3)), bbox_inches='tight')
        i += 1
        plt.close(fig)
    # 获取下一batch的训练集数据
    X_mb, _ = mnist.train.next_batch(mb_size)
    # 根据损失函数，优化生成器关于训练数据的判别和对生成数据的判别
    _, D_loss_curr = sess.run([D_optimizer, D_loss], feed_dict={
                              X: X_mb, Z: sample_Z(mb_size, Z_dim)})
    _, G_loss_curr = sess.run([G_optimizer, G_loss], feed_dict={
                              Z: sample_Z(mb_size, Z_dim)})

    if it % 1000 == 0:
        print('Iter: {}'.format(it))
        print('D loss: {:.4}'.format(D_loss_curr))
        print('G_loss: {:.4}'.format(G_loss_curr))
        print()