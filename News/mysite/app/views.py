from django.shortcuts import render, get_object_or_404
import jieba
import time
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Word, Article
import re
import time
def redtitle(text, wordlist):
    newtext = text
    for word in wordlist:
        if newtext.find(word) != -1:
            newtext = newtext.replace(word, '<font color="#FF3300">'+word+'</font>')
    return newtext

def redtext(text, wordlist):
    newtext = text
    minpos = 1000000
    for word in wordlist:
        tmp = newtext.find(word)
        if tmp != -1:
            if tmp < minpos:
                minpos = tmp
    if minpos > 10:
        newtext = newtext[minpos-10:minpos+190]
    else:
        newtext = newtext[0:200]
    for word in wordlist:
        if newtext.find(word) != -1:
            newtext = newtext.replace(word, '<font color="#FF3300">'+word+'</font>')
    return newtext

# enter the initial page
def index(request):
	articlelist = Article.objects.all()
	dicts = [{'id':each.article_id, 'title':each.article_title, 'text':each.article_text[:150],'time':each.article_time} for each in articlelist]
	if len(articlelist):
		paginator = Paginator(dicts, 20)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
			contacts = paginator.page(1)
		except EmptyPage:
			contacts = paginator.page(paginator.num_pages)
		print(time.strftime('%Y-%m-%d %H:%M:%S'))
		return render(request, 'app/index.html', {'num': len(articlelist), 'text':"", 'contacts': contacts})

# return the search content
def search(request):
    text = request.GET['text']
    if 'select' not in request.GET.keys():
    	order = "all"
    else:
    	order = request.GET['select']
    print(text)
    if text:
        return HttpResponseRedirect(reverse('app:result', args=(text,order)))
    else:
        return HttpResponseRedirect(reverse('app:index'))

def result(request,text,order):
	try:
		words = text.split(" ")
		wordlist = []
		for eachword in words:
			wordlist.extend(list(jieba.lcut(eachword)))
		wordlist = list(set(wordlist))
		print(wordlist)
		print(time.strftime('%Y-%m-%d %H:%M:%S'))
		articlelist = set()
		#search time limits
		deltaday = 7300
		allorder = True
		yearorder = False
		monthorder = False
		weekorder = False
		if order == 'all':
			deltaday = 7300
			allorder = True
		if order == 'year':
			deltaday = 365
			yearorder = True
		if order == 'month':
			deltaday = 30
			monthorder = True
		if order == 'week':
			deltaday = 7
			weekorder = True
		for each_word in wordlist:
			curWord = Word.objects.get(pk = each_word)
			if articlelist:
				articlelist = articlelist&set(curWord.article.filter(article_time__gte=datetime.date.today()-datetime.timedelta(deltaday)))
			else:
				articlelist = set(curWord.article.filter(article_time__gte=datetime.date.today()-datetime.timedelta(deltaday)))
		articlelist = list(articlelist)
		time_start=time.time();
		print(time.strftime('%Y-%m-%d %H:%M:%S'))
		articlelist = sorted(articlelist, key=lambda x:x.article_time, reverse=True)
		dicts = [{'id':each.article_id,'url':each.article_url, 'title':redtitle(each.article_title, wordlist), 'text':redtext(each.article_text, wordlist)} for each in articlelist]
		if len(articlelist):
			paginator = Paginator(dicts, 20)
			page = request.GET.get('page')
			try:
				contacts = paginator.page(page)
			except PageNotAnInteger:
				contacts = paginator.page(1)
			except EmptyPage:
				contacts = paginator.page(paginator.num_pages)
			print(time.strftime('%Y-%m-%d %H:%M:%S'))
			time_end=time.time()
			cost_time = time_end-time_start
			print("cost_time",cost_time)
			return render(request, 'app/result.html', {'num': len(articlelist), 'text': text, 'contacts': contacts, 'all':allorder, 'year':yearorder, 'month':monthorder, 'week':weekorder,'time':cost_time})
		else:
			return HttpResponseRedirect(reverse('app:notfound'))
	except:
		return HttpResponseRedirect(reverse('app:notfound'))

def notfound(request):
	return render(request,'app/notfound.hmtl')

def jump(request,id):
	print(id)
	article = get_object_or_404(Article,pk = id)
	sim = article.article_sim.split(',')
	article1 = get_object_or_404(Article,pk = sim[0])
	article2 = get_object_or_404(Article,pk = sim[1])
	article3 = get_object_or_404(Article,pk = sim[2])
	return render(request,'app/jump.html',{'id':article.article_id, 'title':article.article_title, 'text':article.article_text,'time':article.article_time,'article1':article1,'article2':article2,'article3':article3,'text1':article1.article_text[:100],'text2':article2.article_text[:100],'text3':article3.article_text[:100]})

