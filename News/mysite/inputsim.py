#导入相似新闻id到数据库
import pickle

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

resultlist = []
from app.models import Word, Article
try:
    with open("similarity4.pickle","rb") as file:
        resultlist = pickle.load(file)
except IOError:
    print("Can't open the file:similarity4.pickle")

i = 0
for arti in resultlist:
    print(i)
    ftuple = arti[0]
    curid , score = ftuple[0],ftuple[1]
    inputstr = []
    for index in range(1,4):
        inputstr.append(arti[index][0])
    Article.objects.filter(article_id=curid).update(article_sim=",".join(inputstr))
    i += 1

print("done")
