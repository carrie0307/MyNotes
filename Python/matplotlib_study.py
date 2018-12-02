# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt 
import numpy as np 
from mpl_toolkits.mplot3d import Axes3D

'''
参考资料： 莫烦Python https://morvanzhou.github.io/tutorials/data-manipulation/plt/

重要函数：
plt.xlim() # x轴坐标范围
plt.ylim() # y轴坐标范围

plt.xticks(())  # ignore xticks
plt.yticks(())  

plt.show()

# 绘制标注，x,y是坐标值,ha(horizontal alignmentva)和vap(vertical alignment)表示位置
plt.text(x, y, '%.2f' % y, ha='center', va='bottom'/'top')

# 散点图 s,点大小;c,点颜色;marker,点形状（o,x,*><^）,alpha,点透明度;label,标签
plt.scatter(X, Y, s=75, c=T, alpha=.5)
# 柱状图
plt.bar(X,Y)
# 合图/子图
plt.subplot(221)
ax = fig.add_subplot(111) 
# 曲线图
plt.plot(x, y, color='red', linewidth=1.0, linestyle='--')  

'''

"""一般曲线图"""
x = np.linspace(-3, 3, 50)
y = 2*x + 1
plt.figure()
plt.plot(x, y, color='red', linewidth=1.0, linestyle='--')
plt.show()

"""散点图"""
n = 1024    # data size
X = np.random.normal(0, 1, n) # 每一个点的X值
Y = np.random.normal(0, 1, n) # 每一个点的Y值
X = np.linspace(-3, 3, 50)
Y = 2*x + 1
T = np.arctan2(Y,X) # for color value

plt.scatter(X, Y, s=75, c=T, alpha=.5)

plt.xlim(-1.5, 1.5) # 设置x轴坐标
plt.xticks(())  # ignore xticks
plt.ylim(-1.5, 1.5) # 设置x轴坐标
plt.yticks(())  # ignore yticks

plt.show()

"""柱状图"""
n = 12
X = np.arange(n)
Y1 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
Y2 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
# plt.bar(X,Y)
# facecolor,设置主体色; edgecolor,设置边框
plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

plt.xlim(-.5, n)
plt.ylim(-1.25, 1.25)

plt.xticks(())
plt.yticks(())
# 标注文字
for x, y in zip(X, Y1):
    # ha: horizontal alignment
    # va: vertical alignment
    plt.text(x + 0.4, y + 0.05, '%.2f' % y, ha='center', va='bottom')

for x, y in zip(X, Y2):
    # ha: horizontal alignment
    # va: vertical alignment
    plt.text(x + 0.4, -y - 0.05, '%.2f' % y, ha='center', va='top')

plt.show()

""" 绘制3D坐标轴 """
fig = plt.figure()
ax = Axes3D(fig)
# X, Y value
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
# 产生一个以向量x为行，向量y为列的矩阵
X, Y = np.meshgrid(X, Y)    # x-y 平面的网格
print (X)
print (Y)
R = np.sqrt(X ** 2 + Y ** 2)
# height value
Z = np.sin(R)
# 做出一个三维曲面，并将一个 colormap rainbow 填充颜色
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))
# 如果 zdir 选择了x，那么效果将会是对于 XZ 平面的投影，效果如下
ax.contourf(X, Y, Z, zdir='x', offset=-2, cmap=plt.get_cmap('rainbow'))
plt.show()


""" 多合一显示 """
plt.figure()
'''
# 使用plt.subplot,创建小图;
# plt.subplot(221)表示将整个图像窗口分为2行2列, 当前位置为1;
# 使用plt.plot([0,1],[0,1])在第1个位置创建一个小图.
'''
plt.subplot(221)
plt.plot([0,1],[0,1])
'''
使用plt.subplot,创建小图;
plt.subplot(222)表示将整个图像窗口分为2行2列, 当前位置为2;
使用plt.plot([0,1],[0,2])在第2个位置创建一个小图.
'''
plt.subplot(222)
plt.plot([0,1],[0,2])
'''
使用plt.subplot,创建小图;
plt.subplot(223)表示将整个图像窗口分为2行2列, 当前位置为3;
使用plt.plot([0,1],[0,3])在第3个位置创建一个小图.
'''
plt.subplot(223)
plt.plot([0,1],[0,3])
'''
使用plt.subplot,创建小图;
plt.subplot(224)表示将整个图像窗口分为2行2列, 当前位置为4;
使用plt.plot([0,1],[0,4])在第4个位置创建一个小图.
'''
plt.subplot(224)
plt.plot([0,1],[0,4])
# 展示
plt.show()

""" 多合一显示 - 不均匀制图 """
plt.subplot(211)
plt.plot([0,1],[0,1])

plt.subplot(234)
plt.plot([0,1],[0,2])

plt.subplot(235)
plt.plot([0,1],[0,3])

plt.subplot(236)
plt.plot([0,1],[0,4])

plt.show()  # 展示


""" 同一图上绘制不同曲线 """
x = np.arange(0, 100)   
fig = plt.figure() 
# 注意add_subplot()的使用以及add_subplot()参数含义同plt.subplot()
ax1 = fig.add_subplot(111)     
ax1.scatter([1,3,5],[2,4,6], s = 30, c = 'red', marker = 's')
ax1.plot(x, np.log(x))   
plt.show() 