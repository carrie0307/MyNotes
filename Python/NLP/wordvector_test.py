# -*- coding:utf-8 -*-
"""
对文档进行词袋模型和tfidf模型编码；
gensim.word2vec的一些基本函数(https://blog.csdn.net/MebiuW/article/details/52303622)

词向量：来自词汇表的单词或短语被映射到实数的向量
注意区分词向量和借助词向量将一个句子或文档向量化
"""

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import jieba
from gensim.models import word2vec

corpus = ["我来到北京清华大学北京",
	    "他来到了网易杭研大厦",
	    "小明硕士毕业与中国科学院",
	    "我爱北京天安门"
	    ]

en_corpus = [["I", "came", "to", "TsingHua University", "in", "Beijing"],
             ["He","came", "to", "Ebay", "Hall", "in", "Hangzhou"],
             ["I", "love", "Beijing", "Tian'an Men Square"]
             ]

def getWordbagVec(textLines):
	"""
	词袋模型: 在词集的基础上如果一个单词在文档中出现不止一次，统计其出现的次数（频数）
	功能：使用sklearn.feature_extraction.text.CountVectorizer,通过词袋模型对文本进行表示
	param: textLines: [line1,line2, ...] line是未进行分词处理的句子或文档
	return: wordbagVec:[[],[],[],...] wordbagVec[i]是textLines[i]的基于词袋模型的表示
	
	jieba.cut()使用范例
	fseg_list = jieba.cut(textline, cut_all=False, HMM = False)
	"""
	# 分词：这里尝试了不用全模式效果较好
	word_corpus = [(' ').join(jieba.cut(line)) for line in textLines]
	vectorizer = CountVectorizer()
	word_bag_vec = vectorizer.fit_transform(word_corpus) # 得到词频矩阵
	feature_name = vectorizer.get_feature_names()
	print (feature_name)
	wordbagVec = word_bag_vec.toarray()
	print (wordbagVec)
	return wordbagVec


def getTfIdfVec(textLines):
    """
    TF-IDF模型: TF-IDF是一种统计方法，用以评估某一字词对于一个文件集或一个语料库的重要程度。
    字词的重要性随着它在文件中出现的次数成正比增加，但同时会随着它在语料库中出现的频率成反比下降。

    功能：使用sklearn.feature_extraction.text.CountVectorizer和TfidfTransformer()，通过td-idf对文本进行表示
    param: textLines: [line1,line2, ...] line是未进行分词处理的句子或文档
    return: tfidfVec:[[],[],[],...] tfidfVec[i]是textLines[i]的基于tf-idf的表示
    """
    word_corpus = [(' ').join(jieba.cut(line)) for line in textLines]
    vectorizer = CountVectorizer()
    word_bag_vec = vectorizer.fit_transform(word_corpus) # 得到词频矩阵
    transformer = TfidfTransformer()#该类会统计每个词语的tf-idf权值
    tfidfVec =transformer.fit_transform(word_bag_vec)
    tfidfVec = tfidfVec.toarray()
    return tfidfVec

def useWord2Vec(textLines):
    """
    使用gensim的wrod2Vec进行
    """
    # Word2Vec()参数解释:https://blog.csdn.net/mpk_no1/article/details/72510655
    # 训练一个Word2Vec模型
    """处理英文"""
    model_en = word2vec.Word2Vec(en_corpus, min_count=1)
    print (model_en.similarity('Beijing', 'Hangzhou'))
    print (model_en['Beijing'])

    # 保存训练好的模型
    # model.save_word2vec_format(outp2, binary=False)  
    # 加载训练好的模型
    # model = word2vec.load("D:/data/wiki2vector/en_1000_no_stem/en.model")
    
    word_corpus = [list(jieba.cut(line)) for line in textLines]
    model = word2vec.Word2Vec(word_corpus, min_count=1)  # 默认window=5
    # 1. 获取两个词之间的相似度
    print (model.similarity('北京', '天安门'))
    # 2. 获取某个词的词向量
    print (model['北京'])
    # 3. 使用某些词语来限定，分正向和负向(例如下例的含义是，与'北京', '天安门'最相似，与'清华大学']最不相似的)
    model.most_similar(positive=['北京', '天安门'], negative=['清华大学'])
    # 4. 从一堆词里面找到不匹配的
    print ("北京 天安门 网易 , 有哪个是不匹配的? word2vec结果说是:"+model.doesnt_match("北京 天安门 网易".split()))
    # 可参见https://blog.csdn.net/MebiuW/article/details/52303622

    # 注意https://github.com/fishyyh/CNN-SQL/blob/master/word.py，在model.build_vocab()才加上了sentences参数， model = word2vec.Word2Vec并未添加sentence语料
    

if __name__ == '__main__':
	# getWordbagVec(corpus)
    # getTfIdfVec(corpus)
    useWord2Vec(corpus)