import cPickle
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","mysite.settings")
django.setup()
from app.models import Word, Article

WordDict = {}

try:
    with open("../WordFile.pickle", "rb") as WordFile:
        WordDict = cPickle.load(WordFile)
except:
    print "IOError"

i = 0
for each_word in WordDict:
    if i%100 == 0:
        print i
    #article_list = WordDict[each_word]
    Word.objects.create(word_text=each_word)
    #articlelist = []
    #for each_ID in article_list:
        #articlelist.append(Article.objects.get(pk=each_ID))
        #if len(articlelist) == 10000:
            #print len(articlelist)
            #curWord.article.add(*articlelist)
            #articlelist = []
    #rint len(articlelist)
    #curWord.article.add(*articlelist)
    i += 1

