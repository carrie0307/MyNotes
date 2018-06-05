
#coding: utf-8
import os
import time
import random
import jieba
# import nltk
import sklearn
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

"""
zip(*list)相当于解压操作，eg. li = [([1, 2, 3], 0), ([2, 3, 4], 1)], a,b = zip(*li),
>>> a=([1, 2, 3], [2, 3, 4]),b=(0, 1)
"""

"""
代码来自：
https://github.com/lining0806/Naive-Bayes-Classifier
流程：
1. 遍历所有文件，构建每个文件的词袋模型(jieba分词)
2. 遍历以上每个文件的词袋模型结果，构建测试集和训练集；并统计针对所有文件的词袋模型，并统计每个词出现次数；
3. 根据所有文件的词袋模型，计算训练集、测试集每个文件的向量表示[用0,1表示词袋模型中的词是否在某个文件中出现]；
4. 使用sklearn中的MultinomialNB多项式贝叶斯进行分类

关键词:分词；词袋模型；每篇文章的向量表示；贝叶斯分类
"""


def MakeWordsSet(words_file):
    """
    功能：读取文件，对词进行去重
    """
    words_set = set()
    with open(words_file, 'r') as fp:
        for line in fp.readlines():
            word = line.strip().decode("utf-8")
            if len(word)>0 and word not in words_set: # 去重
                words_set.add(word)
    return words_set

def TextProcessing(folder_path, test_size=0.2):
    """
    param:folder_path:
    param:test_size:测试集所占比例
    return:all_words_list:             所有词的集合 ？？？
    return:train_data_list:训练集数据
    return:test_data_list:测试集数据
    return: train_class_list:训练集标签
    return:test_class_list:测试集标签
    """
    folder_list = os.listdir(folder_path)
    data_list = []
    class_list = []

    # 类间循环
    for folder in folder_list:
        new_folder_path = os.path.join(folder_path, folder)
        files = os.listdir(new_folder_path)
        # 类内循环
        j = 1
        for file in files:
            if j > 100: # 每类text样本数最多100
                break
            with open(os.path.join(new_folder_path, file), 'r') as fp:
               raw = fp.read()
            # print raw
            ## --------------------------------------------------------------------------------
            ## jieba分词
            # jieba.enable_parallel(4) # 开启并行分词模式，参数为并行进程数，不支持windows
            word_cut = jieba.cut(raw, cut_all=False) # 精确模式，返回的结构是一个可迭代的genertor
            word_list = list(word_cut) # genertor转化为list，每个词unicode格式
            # jieba.disable_parallel() # 关闭并行分词模式
            # print word_list
            ## --------------------------------------------------------------------------------
            data_list.append(word_list)
            class_list.append(folder.decode('utf-8'))
            j += 1

    ## 划分训练集和测试集
    # train_data_list, test_data_list, train_class_list, test_class_list = sklearn.cross_validation.train_test_split(data_list, class_list, test_size=test_size)
    data_class_list = zip(data_list, class_list)
    random.shuffle(data_class_list)
    # 根据设定的test_size划分测试集数据范围,用Index作为分割
    index = int(len(data_class_list)*test_size)+1
    train_list = data_class_list[index:]
    test_list = data_class_list[:index]
    # zip(*list)相当于解压操作，eg. li = [([1, 2, 3], 0), ([2, 3, 4], 1)], a,b = zip(*li),
    # >>> a=([1, 2, 3], [2, 3, 4]),b=(0, 1)
    train_data_list, train_class_list = zip(*train_list)
    test_data_list, test_class_list = zip(*test_list)

    # 统计词频放入all_words_dict
    all_words_dict = {}
    for word_list in train_data_list:
        # word_list应该是每一篇文章的词袋集合
        for word in word_list:
            if all_words_dict.has_key(word):
                all_words_dict[word] += 1
            else:
                all_words_dict[word] = 1
    # key函数利用词频进行降序排序
    all_words_tuple_list = sorted(all_words_dict.items(), key=lambda f:f[1], reverse=True) # 内建函数sorted参数需为list
    all_words_list = list(zip(*all_words_tuple_list)[0])

    return all_words_list, train_data_list, test_data_list, train_class_list, test_class_list


def words_dict(all_words_list, deleteN, stopwords_set=set()):
    """
    param:
    """
    # 选取特征词
    feature_words = []
    n = 1
    for t in range(deleteN, len(all_words_list), 1):
        # n是记录feature_words的计数器，根据all_word_list，这里取出现次数前1000的词作为特征项
        if n > 1000: # feature_words的维度1000
            break
        # print all_words_list[t]
        if not all_words_list[t].isdigit() and all_words_list[t] not in stopwords_set and 1<len(all_words_list[t])<5:
            feature_words.append(all_words_list[t])
            n += 1
    return feature_words


def TextFeatures(train_data_list, test_data_list, feature_words, flag='nltk'):
    """
    生成每篇文章的特征向量
    param:train_data_list:训练数据集
    param:test_data_list:测试数据集
    param:feature_words:特征词列表
    param:flag: 方法
    return:train_feature_list:训练数据集特征向量
    return:test_feature_list:测试数据集特征向量
    """

    def text_features(text, feature_words):
        """
        生成单篇文章的特征向量 用1或0表示text中是否包含特征词
        """
        text_words = set(text)
        ## -----------------------------------------------------------------------------------
        if flag == 'nltk':
            ## nltk特征 dict
            features = {word:1 if word in text_words else 0 for word in feature_words}
        elif flag == 'sklearn':
            ## sklearn特征 list
            features = [1 if word in text_words else 0 for word in feature_words]
        else:
            features = []
        ## -----------------------------------------------------------------------------------
        return features

    train_feature_list = [text_features(text, feature_words) for text in train_data_list]
    test_feature_list = [text_features(text, feature_words) for text in test_data_list]
    return train_feature_list, test_feature_list


def TextClassifier(train_feature_list, test_feature_list, train_class_list, test_class_list, flag='nltk'):
    """
    param:train_feature_list
    param:test_feature_list
    param:train_class_list
    param:test_class_list
    param:flag='nltk':方法

    """
    ## -----------------------------------------------------------------------------------
    # if flag == 'nltk':
    #     ## nltk分类器
    #     train_flist = zip(train_feature_list, train_class_list)
    #     test_flist = zip(test_feature_list, test_class_list)
    #     classifier = nltk.classify.NaiveBayesClassifier.train(train_flist)
    #     # print classifier.classify_many(test_feature_list)
    #     # for test_feature in test_feature_list:
    #     #     print classifier.classify(test_feature),
    #     # print ''
    #     test_accuracy = nltk.classify.accuracy(classifier, test_flist)
    # elif flag == 'sklearn':
    if flag == 'sklearn':
        ## sklearn分类器
        # http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html#sklearn.naive_bayes.MultinomialNB
        # 多项分别贝叶斯分类器
        classifier = MultinomialNB().fit(train_feature_list, train_class_list)
        # print classifier.predict(test_feature_list)
        # for test_feature in test_feature_list:
        #     print classifier.predict(test_feature)[0],
        # print ''
        test_accuracy = classifier.score(test_feature_list, test_class_list)
    else:
        test_accuracy = []
    return test_accuracy


if __name__ == '__main__':

    print ("start")

    ## 文本预处理
    folder_path = './Database/SogouC/Sample'
    all_words_list, train_data_list, test_data_list, train_class_list, test_class_list = TextProcessing(folder_path, test_size=0.2)

    # 生成stopwords_set
    stopwords_file = './stopwords_cn.txt'
    stopwords_set = MakeWordsSet(stopwords_file)

    ## 文本特征提取和分类
    # flag = 'nltk'
    flag = 'sklearn'
    deleteNs = range(0, 1000, 20)
    test_accuracy_list = []
    for deleteN in deleteNs:
        # feature_words = words_dict(all_words_list, deleteN)
        feature_words = words_dict(all_words_list, deleteN, stopwords_set)
        # 得到每篇文章的特征向量
        train_feature_list, test_feature_list = TextFeatures(train_data_list, test_data_list, feature_words, flag)
        test_accuracy = TextClassifier(train_feature_list, test_feature_list, train_class_list, test_class_list, flag)
        test_accuracy_list.append(test_accuracy)
    print (test_accuracy_list)

    # 结果评价
    plt.figure()
    plt.plot(deleteNs, test_accuracy_list)
    plt.title('Relationship of deleteNs and test_accuracy')
    plt.xlabel('deleteNs')
    plt.ylabel('test_accuracy')
    plt.savefig('result.png')

    print ("finished")