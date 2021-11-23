import sqlite3
import sys

# 计算词向量之间的相似度
sys.path.append('..')
from text2vec import SBert, cos_sim

# Load pre-trained Sentence Transformer Model (based on DistilBERT). It will be downloaded automatically
model = SBert('paraphrase-multilingual-MiniLM-L12-v2')

conn = sqlite3.connect('data.db')
cursor = conn.execute("select tag, count(tag) as num from video_info group by tag")
kind = []
kind_num = []
for it in cursor:
    kind.append(it[0])
    kind_num.append(it[1])

conn.commit()
conn.close()

# Two lists of sentences
sentences1 = kind

sentences2 = ['MV','舞蹈' ,'健身', '影视','音乐', '生活' ,'动物', '手办' ,'数码' ,'鬼畜' ,'搞笑' ,'汽车'
       , '游戏' , '体育' ,'知识' ,'穿搭' ,'美食' ,'计算机']


# Compute embedding for both lists
embeddings1 = model.encode(sentences1)
embeddings2 = model.encode(sentences2)

# Compute cosine-similarits
cosine_scores = cos_sim(embeddings1, embeddings2)

KindMap = {}
# Output the pairs with their score
for i in range(len(sentences1)):
    max = 0
    for j in range(len(sentences2)):
        print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[j], cosine_scores[i][j]))
        if cosine_scores[i][j]>max:
            max = cosine_scores[i][j]
            index = j
    KindMap[sentences1[i]]=sentences2[index]
print(KindMap)

