import cPickle
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","mysite.settings")
django.setup()
from app.models import Word, Article

articleDict = {}

try:
    with open("../ArticleFile1.pickle", "rb") as ArticleFile:
        articleDict = cPickle.load(ArticleFile)
except:
    print "IOError"

i = 0
for each_ID in articleDict:
    print "1", i
    curArticle = Article.objects.get(pk=each_ID)
    wordlist = []
    for each_word in articleDict[each_ID]:
        try:
            wordlist.append(Word.objects.get(pk=each_word))
        except:
            print "error"
        if len(wordlist) == 500:
            curArticle.word_set.add(*wordlist)
            wordlist = []
    curArticle.word_set.add(*wordlist)
    i += 1

articleDict = {}

try:
    with open("../ArticleFile2.pickle", "rb") as ArticleFile:
        articleDict = cPickle.load(ArticleFile)
except:
    print "IOError"

i = 0
for each_ID in articleDict:
    print "2", i
    curArticle = Article.objects.get(pk=each_ID)
    wordlist = []
    for each_word in articleDict[each_ID]:
        try:
            wordlist.append(Word.objects.get(pk=each_word))
        except:
            print "error"
        if len(wordlist) == 500:
            print "500"
            curArticle.word_set.add(*wordlist)
            wordlist = []
    print len(wordlist)
    curArticle.word_set.add(*wordlist)
    i += 1

