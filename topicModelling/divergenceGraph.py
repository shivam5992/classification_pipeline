from gensim import corpora, models, similarities, matutils
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os 

input_file = "/media/inno/01D04251141467101/WKData/cleanPipeline/"
relevant = ["060-Health insurance  or  insurers"]
limit = 200




def sym_kl(p, q):
    return np.sum([stats.entropy(p, q),stats.entropy(q, p)])    

texts = []
all_files = os.listdir(input_file)
for folder in all_files:
    if folder in relevant:
        for file in os.listdir(input_file + "/" + folder)[:limit]:
            path = input_file + folder +"/"+ file
            document = open(path).read() 
            texts.append(document.split())

# temp = []
# for i,j in enumerate(texts):   
#     temp1 = []
#     l = len(j)
#     for i1 in range(l-1):
#         s = str(j[i1] + ' ' + j[i1+1])
#         temp1.append(s)
#     temp.append(temp1)
# texts = temp
dictionary = corpora.Dictionary(texts)
dictionary.compactify()

class MyCorpus(object):
    def __iter__(self):
        for folder in all_files:
            if folder in relevant:
                for file in os.listdir(input_file + "/" + folder)[:limit]:
                    path = input_file + folder +"/"+ file
                    document = open(path).read() 
                    yield dictionary.doc2bow(document.split())
        
        # for line in open(input_file):
            # yield dictionary.doc2bow(line.lower().split())

my_corpus = MyCorpus()
l = np.array([sum(cnt for _, cnt in doc) for doc in my_corpus])

def arun(corpus, dictionary, max_topics, min_topics=1, step=1):
    kl = []
    for i in range(min_topics,max_topics,step):
        lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=i)
        m1 = lda.expElogbeta
        U, cm1, V = np.linalg.svd(m1)
        lda_topics = lda[my_corpus]
        m2 = matutils.corpus2dense(lda_topics, lda.num_topics).transpose()
        cm2 = l.dot(m2)        
        cm2 = cm2 + 0.0001
        cm2norm = np.linalg.norm(l)
        cm2 = cm2/cm2norm
        kl.append(sym_kl(cm1,cm2))
    return kl
    
kl = arun(my_corpus, dictionary, max_topics=100)
plt.plot(kl)
plt.ylabel('Symmetric KL Divergence')
plt.xlabel('Number of Topics')
plt.savefig('kldiv500.png', bbox_inches='tight')