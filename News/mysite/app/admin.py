from django.contrib import admin
from .models import Article, Word

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['article_title', 'article_text', 'article_time', 'article_url', 'article_id']})
    ]
    list_display = ('article_title', 'article_id', 'article_time')
    list_filter = ['article_time']
    search_fields = ['article_text']

class WordAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['word_text']})
    ]
    search_fields = ['word_text']
admin.site.register(Article, ArticleAdmin)
admin.site.register(Word, WordAdmin)