#coding=utf-8
import urllib.request,urllib.error,urllib.parse
import re
from html.parser import HTMLParser
import os
import pickle
# 存储所有从页面中获得的URL ， 作为一个队列， 初始为根节点
linkList = ["/index.html"]
prevUrl = "http://news.tsinghua.edu.cn/publish/thunews"
# 以页面ID 为索引， 存储标题、正文、时间、路径
IDDict = {}
# 定义MyHTMLParser 类用来分析HTML 文本， 获取时间、标题、正文
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.articleFlag = False
        self.titleFlag = False
        self.title = ""
        self.text = ""
        self.time = []

    def handle_starttag(self, tag, attrs):
        if tag == "article":
            self.articleFlag = True
        if tag == "title":
            self.titleFlag = True

    def handle_endtag(self, tag):
        if tag == "article":
            self.articleFlag = False
        if tag == "title":
            self.titleFlag = False

    def handle_data(self, data):
        if self.articleFlag:
            self.text += re.compile("[\s]*").sub("", data)
        if self.titleFlag:
            self.title += re.compile("[\s]*").sub("", data)

    def get_text(self):
        return self.text

    def get_time(self):
        tmpResult = re.compile("(\d{4})\xe5\xb9\xb4(\d{2})\xe6\x9c\x88(\d{2})\xe6\x97\xa5(\d{2}):(\d{2}):(\d{2})", re.L).search(self.text)
        if tmpResult:
            self.time.extend(
            [tmpResult.group(1), tmpResult.group(2), tmpResult.group(3), tmpResult.group(4), tmpResult.group(5), tmpResult.group(6)])
        return self.time

    def get_title(self):
        return self.title
# 将HTML 文本中的时间、标题、正文提取出来
def getHtml(url):
    request = urllib.request.Request(prevUrl+url)
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        print (e.code)
        return None
    except urllib.error.URLError as e:
        print (e.reason)
        return None
    else:
        html = response.read().decode("utf-8")
        return html

def getLink(html):
    if html:
        reg = re.compile(r"href=\"/publish/thunews(/.+?\.html)\"")
        return re.findall(reg, html)
    else:
        return None

def getID(url):
    tmpResult = re.compile("/(\d{7,})/").search(url)
    if tmpResult:
        return tmpResult.group(1)
    else:
        return None

def readHtml(html):
    try:
        parser = MyHTMLParser()
        parser.feed(html)
        return (parser.get_title(), parser.get_text(), parser.get_time())
    except UnicodeError:
        print("codeError")
        return None


i = 0
while i < len(linkList):
    print(i, linkList[i])
    tmpHtml = getHtml(linkList[i])
    tmpID = getID(linkList[i])
    if tmpID and tmpHtml:
        tmpText = readHtml(tmpHtml)
        if tmpText:
            IDDict[tmpID] = {'url': linkList[i], 'title': tmpText[0], 'text': tmpText[1], 'time': tuple(tmpText[2])}
    l = getLink(tmpHtml)
    if l:
        for each_link in l:
            if linkList.count(each_link) == 0:
                linkList.append(each_link)
    i += 1

try:
    with open("IDFile.pickle", "wb") as IDFile:
        pickle.dump(IDDict, IDFile)
except IOError:
    print("Can't open the file: IDFile.pickle")

try:
    with open("IDFile.txt", "w") as IDTxt:
        for i in IDDict.keys():
            IDTxt.write(i+"\n"+prevUrl+IDDict[i]['url']+"\n"+IDDict[i]['title']+"\n"+IDDict[i]['text']+"\n"+str(IDDict[i]['time'])+"\n\n")
except IOError:
    print ("Can't open the file: IDFile.txt")