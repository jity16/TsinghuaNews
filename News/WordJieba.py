#coding=utf-8
import pickle
import jieba

IDDict = {}
wordDict = {}
try:
    with open("IDFile.pickle", "rb") as IDFile:
        IDDict = pickle.load(IDFile)
except IOError:
    print ("Can't open the file: IDFile.pickle")

i = 0
for each_ID in IDDict.keys():
    if i % 100 == 0:
        print(i)
    wordList = [each_cut.encode("utf-8") for each_cut in jieba.lcut_for_search(IDDict[each_ID]['text'])]
    wordList.extend([each_cut.encode("utf-8") for each_cut in jieba.lcut_for_search(IDDict[each_ID]['title'])])
    wordList = list(set(wordList))
    for each_word in wordList:
        if each_word not in wordDict.keys():
        #if not wordDict.has_key(each_word):
            wordDict[each_word] = []
        wordDict[each_word].append(each_ID)
    i += 1

try:
    with open("WordFile.pickle", "wb") as wordFile:
        pickle.dump(wordDict, wordFile)
except IOError:
    print ("Can't open the file: WordFile.pickle")

try:
    with open("WordFile.txt", "w") as wordTxt:
        for i in wordDict.keys():
            wordTxt.write(i.decode("utf-8")+"\n"+str(wordDict[i])+"\n\n")
except IOError:
    print ("Can't open the file: IDFile.txt")