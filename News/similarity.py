#计算相似度
import pickle
import math
import jieba
import gensim
from collections import defaultdict
from gensim import corpora,models,similarities

fileaddr = 'C:/Users/DELL/Desktop/News'


IDDict = {}
WordDict = {}
try:
    with open("IDFile.pickle", "rb") as IDFile:
        IDDict = pickle.load(IDFile)
except IOError:
    print ("Can't open the file: IDFile.pickle")

print("all doc size = ",len(IDDict))

docsize=len(IDDict)

#documents = [IDDict[key]['text'] for key in IDDict.keys()]
#print("documents size=",len(documents))

documents = []
index2idDict = {}
i = 0
for key in IDDict.keys():
    documents.append(IDDict[key]['text'])
    index2idDict[i]=key
    i = i+1
print("documents size=",len(documents))
#保存index 到 id 的字典  便于找到对应的文章
try:
    with open(fileaddr+"Index2IdDict.pickle", "wb") as i2ifile:
        pickle.dump(index2idDict, i2ifile)
except IOError:
    print("Can't open the file: Index2IdDict.pickle")
print("Index2IdDict.pickle保存完毕 位置:C:/Users/DELL/Desktop/News/Index2IdDict.pickle")

try:
    with open("WordFile.pickle","rb") as WordFile:
        WordDict = pickle.load(WordFile)
except IOError:
    print ("Can't open the file: WordFile.pickle")

print("all term size = ",len(WordDict))

wordlist = list(WordDict.keys())

#对所有文章进行分词操作

texts = [jieba.lcut_for_search(document) for document in documents]

print("分词操作完成")

#去掉无用词
stoplist = list(', . ( ) 的 地 和 你 它 我 他 是 。 ， + - * / : ; [ ] = ! ~ ? < >'.split(" "))
texts = [word for word in texts if word not in stoplist]

print("无用词清除结束")

dictionary = gensim.corpora.Dictionary(texts)

print("词典生成完毕")

dictionary.save(fileaddr+"worddict.dict")

print("词典保存完毕 位置:%sworddict.dict" % fileaddr)

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize(fileaddr+'mmcorpus.mm',corpus)
print("corpus保存完毕 位置:%smmcorpus.mm" %fileaddr)



#corpus = corpora.MmCorpus(fileaddr+'mmcorpus.mm')
#print("corpus 读取完毕")

lsi_model = models.LsiModel(corpus,id2word=dictionary,num_topics=200)
print("lsi模型生成完毕 num_topics=200")

i = 0
index = similarities.MatrixSimilarity(lsi_model[corpus])
index.save(fileaddr+'index.index')
print("index文件保存完毕 位置:%sindex.index" %fileaddr)
finalsims=[] #二维矩阵
for query in corpus:
    sims = index[lsi_model[query]]
    vec = [] #某一行
    for x in sims:
        vec.append(x)
    finalsims.append(vec)
    print("doc %d done" % i)
    i = i+1

print("相似度计算完毕")


#测试数据合理性
print("---------测试数据合理性")
#对角线元素最大
rlen = len(finalsims)
clen = len(finalsims[0])
print ("行数=%s 列数=%s"%(rlen,clen))

#测试左上角 n*n矩阵
n = 10
for i in range(0,n):
    for j in range(0,n):
        print(finalsims[i][j],end=' ')
    print('\n')
print("-------测试结束--------")

print("计算 前k个相似文章 矩阵为 docsize * k ")
k=4
print("k = ",k)
expectedlist = []
i = 0
for li in finalsims:
    reli = sorted(enumerate(li), key=lambda item: -item[1])[:k]
    expectedlist.append(reli)
    print("row %d done" % i )
    i = i +1


print("计算完成....展示前n个")
for i in range(0,n):
    print(expectedlist[i])

print("将其序号转换为文章id")
resultlist=[]
for li in expectedlist:
    tmplist = []
    for index,item in li:
    	tmplist.append((index2idDict[index],item))
    resultlist.append(tmplist)

print("开始保存最终文件")
try:
    with open(fileaddr+"similarity"+str(k)+".pickle", "wb") as file:
        pickle.dump(resultlist, file)
except IOError:
    print("Can't open the file: similarity%d.pickle" %k)
print("similarity%d.pickle保存完毕 位置:%ssimilarity%d.pickle" %(k,fileaddr,k))
try:
    with open(fileaddr+"similarity"+str(k)+".txt", "w") as file:
        for l in resultlist:
            file.write(str(l)+'\n\n')
except IOError:
    print("Can't open the file: similarity%d.txt" %k)
print("similarity%d.txt保存完毕 位置:%ssimilarity%d.txt" %(k,fileaddr,k))
