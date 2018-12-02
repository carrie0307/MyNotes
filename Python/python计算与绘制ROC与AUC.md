# 绘制ROC曲线

## 根据阈值进行二分类划分的情况下

```python
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
# from sklearn.metrics import roc_curve, auc  ###计算roc和auc

# 注： metrics.roc_curve 只能用于二分类

# 难道不是k折交叉验证时，每次得到一个fpr和tpf，k次的组合得到FPR和TPR列表，然后画图吗？ 一次的结果可以吗？？ 
y = np.array([1, 1, 2, 2])
scores = np.array([0.1, 0.4, 0.35, 0.8])
# scores是该样本判断为positive的概率
# threshhold是判别为positive的阈值
fpr, tpr, thresholds = metrics.roc_curve(y, scores, pos_label=2)
print (fpr)
# fpr = [0.  0.5 0.5 1. ]
print (tpr)
# tpr = [0.5 0.5 1.  1. ]
print (thresholds)
# threshhode = [0.8  0.4  0.35 0.1 ]
'''
例如，当threshhold=0.8时，
根据scores只有最后一个样本被判别为positive, 此时负样本中没有错判为positive的，故fpr=0;
但2个正样本中只有一个被判别为正样本，故tpr=0.5
'''
auc = metrics.auc(fpr, tpr)
print ("auc = {}".format(str(auc)))

# 绘制ROC曲线
plt.plot([0, 1], [0, 1], '--', color=(0 , 0, 1))#画对角线
plt.plot([0, 1], [0, 0], '-', color=(0, 0, 1))#画x轴
plt.plot([1, 1], [0, 1], '-', color=(0, 0, 1))#画边界
plt.plot(fpr, tpr, "r", linewidth=1)#在当前绘图对象绘图，红线
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic curve')
plt.show()#显示图像
```

## 其他情况

其他情况下，只要设法计算出FPR和TPR，然后直接绘制即可.

一般在K折交叉验证时，每一折产生一个fpr和tpr，最后得到FPR和TPR列表