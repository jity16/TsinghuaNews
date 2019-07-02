from django.db import models

# Create your models here.
class Article(models.Model):
	article_id = models.CharField(max_length = 50,primary_key = True)
	article_url = models.CharField(max_length= 200)
	article_title = models.CharField(max_length = 20)
	article_text = models.TextField()
	article_time = models.DateTimeField()
	article_sim = models.CharField(max_length=300)
	def __str__(self):
		return self.article_title

class Word(models.Model):
	word_text = models.CharField(max_length = 200,primary_key = True)
	article = models.ManyToManyField(Article)
	def __str__(self):
		return self.word_text




