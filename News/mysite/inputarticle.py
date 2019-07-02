import cPickle
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","mysite.settings")
django.setup()
from app.models import Article
import datetime

IDDict = {}

prevurl = 'http://news.tsinghua.edu.cn/publish/thunews'

try:
    with open("../IDFile.pickle", "rb") as IDFile:
        IDDict = cPickle.load(IDFile)
except IOError:
    print "IOError"
    
for each_ID in IDDict:
    time = IDDict[each_ID]['time']
    if len(time) == 6:
        times = datetime.datetime(int(time[0]), int(time[1]), int(time[2]), int(time[3]), int(time[4]), int(time[5]))
    else:
        times = datetime.datetime(int(each_ID[0:4]), int(each_ID[4:6]), int(each_ID[6:8]), int(each_ID[8:10]), int(each_ID[10:12]), int(each_ID[12:14]))
    Article.objects.create(article_id=each_ID, article_url=prevurl+IDDict[each_ID]['url'], article_title=IDDict[each_ID]['title'], article_text=IDDict[each_ID]['text'], article_time=times)
