# -*- coding: utf-8 -*-
import xadmin
from .models import *


class ArticleAdmin(object):
    list_display = ['user', 'title', 'desc',  'click_count', 'date_publish']
    search_fields = ['user', 'title', 'desc', 'click_count', 'date_publish']
    list_filter = ['user', 'title', 'desc',  'click_count', 'date_publish']
    style_fields = {"content": "ueditor"}
    # 在增加IDC数据的时候，获取当前登录的用户信息，并保存到user字段里
    # def save_models(self):
    #     self.new_obj.user = self.request.user
    #     super().save_models()

#
# class TagAdmin(object):
#     list_display = ['name']
#     search_fields = ['name']
#     list_filter = ['name']


class CommentAdmin(object):
    # list_display = ['content', 'username', 'date_publish', 'user', 'article']
    list_display = ['username', 'content']
    search_fields = ['content']
    list_filter = ['content']


class KeywordsAdmin(object):
    # list_display = ['content', 'username', 'date_publish', 'user', 'article']
    list_display = ['word']
    search_fields = ['word']
    list_filter = ['word']


xadmin.site.register(Article, ArticleAdmin)
# xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(Keywords, KeywordsAdmin)
