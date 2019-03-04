# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView, VideoPlayView, CourseSearchListView
# 导入view函数
# from users.views import SelectView
# 要写上app的名字
app_name = "course"

urlpatterns = [
    # url(r'^select/course_lesson/', SelectView.as_view(), name='course_lesson'),
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),

    # 课程搜索页面
    url(r'^searchlist/$', CourseSearchListView.as_view(), name='searchlist'),

    #课程详情页
    url(r'detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),

    # 章节信息页
    url(r'info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),

    # 课程评论页
    url(r'comment/(?P<course_id>\d+)/', CommentsView.as_view(), name="course_comments"),

    # 添加评论
    url(r'add_comment/', AddCommentsView.as_view(), name="add_comment"),

    # 视频地址
    url(r'video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name="video_play"),

]