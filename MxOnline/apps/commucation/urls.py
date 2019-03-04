# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import ContentListView, ArticleListView, commentView

app_name = "commucation"

urlpatterns = [
    # 测试地址
    url(r'list/$', ContentListView.as_view(), name="list"),
    # 文章地址
    url(r'article/$', ArticleListView.as_view(), name="article"),
    url(r'^comment/post/$', commentView.as_view(), name='comment_post'),
]