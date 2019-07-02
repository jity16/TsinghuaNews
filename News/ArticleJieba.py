#coding=utf-8
import pickle
import jieba

IDDict = {}
articleDict = {}
try:
    with open("IDFile.pickle", "rb") as IDFile:
        IDDict = pickle.load(IDFile)
except IOError:
    print ("Can't open the file: IDFile.pickle")

IDList = list(IDDict.keys())

for i in range(0, len(IDList)//2):
    if i % 10 == 0:
        print(i)
    wordList = [each_cut.encode("utf-8") for each_cut in jieba.lcut_for_search(IDDict[IDList[i]]['text'])]
    wordList.extend([each_cut.encode("utf-8") for each_cut in jieba.lcut_for_search(IDDict[IDList[i]]['title'])])
    wordList = list(set(wordList))
    articleDict[IDList[i]] = wordList
    i += 1

try:
    with open("ArticleFile1.pickle", "wb") as articleFile:
        pickle.dump(articleDict, articleFile)
except IOError:
    print ("Can't open the file: ArticleFile.pickle")

try:
    with open("ArticleFile1.txt", "w") as articleTxt:
        for i in articleDict.keys():
            articleTxt.write(i+"\n")
            for j in articleDict[i]:
                articleTxt.write(j.decode("utf-8")+" ")
            articleTxt.write("\n\n")
except IOError:
    print ("Can't open the file: ArticleFile.txt")

articleDict = {}

for i in range(len(IDList)//2, len(IDList)):
    if i % 10 == 0:
        print(i)
    wordList = [each_cut.encode("utf-8") for each_cut in jieba.lcut_for_search(IDDict[IDList[i]]['text'])]
    wordList.extend([each_cut.encode("utf-8") for each_cut in jieba.lcut_for_search(IDDict[IDList[i]]['title'])])
    wordList = list(set(wordList))
    articleDict[IDList[i]] = wordList
    i += 1

try:
    with open("ArticleFile2.pickle", "wb") as articleFile:
        pickle.dump(articleDict, articleFile)
except IOError:
    print("Can't open the file: ArticleFile.pickle")

try:
    with open("ArticleFile2.txt", "w") as articleTxt:
        for i in articleDict.keys():
            articleTxt.write(i+"\n")
            for j in articleDict[i]:
                articleTxt.write(j.decode("utf-8")+" ")
            articleTxt.write("\n\n")
except IOError:
    print("Can't open the file: ArticleFile.txt")
