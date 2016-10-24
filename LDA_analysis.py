# -*- coding: utf-8 -*-

'''  
@ Athuor: Tristan SHi
@ Created Date:   24/10/2016
@ Created Time:   7:42 PM
@ Contact: fineshi@foxmail.com
'''
import jieba
import pandas as pd
from gensim import corpora,models

path = ''
df = pd.read_csv(path, encoding='utf-8')

# 评价为4星及以上为正面， 2星及以下为负面
pos = pd.concat([df[df['Rating'] == 5],df[df['Rating'] == 4]])
neg = pd.concat([df[df['Rating'] == 2],df[df['Rating'] == 1]])

# 用于中文分词
mycut = lambda s: ' '.join(jieba.cut(s))
pos['Review_content'] = pos['Review_content'].apply(mycut)
neg['Review_content'] = neg['Review_content'].apply(mycut)

stop = pd.read_csv('stoplist.txt')
stop = [' ', ''] + list(stop[0])

# 建立LDA模型
neg['r'] = neg['Review_content'].apply(lambda s: s.split(' '))
neg['rr'] = neg['r'].apply(lambda x: [i for i in x if i not in stop])

neg_dict = corpora.Dictionary(neg['rr'])
neg_corpus = [neg_dict.doc2bow(i) for i in neg['rr']]
neg_lda = models.LdaModel(neg_corpus, num_topics=10, id2word=neg_dict)

neg_lda.print_topics()


pos['r'] = pos['Review_content'].apply(lambda s: s.split(' '))
pos['rr'] = pos['r'].apply(lambda x: [i for i in x if i not in stop])

pos_dict = corpora.Dictionary(pos['rr'])
pos_corpus = [pos_dict.doc2bow(i) for i in pos['rr']]
pos_lda = models.LdaModel(pos_corpus, num_topics=10, id2word=pos_dict)

pos_lda.print_topics()


