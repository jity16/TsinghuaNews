from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views
import re

app_name = 'app'
urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^search/', views.search, name='search'),
    url(r'^result/(?P<text>.+)/(?P<order>.+)/', views.result, name='result'),
    url(r'^notfound/', views.notfound, name='notfound'),
    url(r'^jump/(\d+)/$',views.jump,name = 'jump')
]
