# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import UserinfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, AddPublishView
from .views import MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView, MyArticleView, DeleteArticleView
# 导入view函数
from users.views import SelectView


urlpatterns = [
    url(r'^select/course_lesson/', SelectView.as_view(), name='course_lesson'),
    #用户信息
    url(r'^info/$', UserinfoView.as_view(), name='user_info'),

    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),

    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),

    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    # 我收藏的课程机构
    url(r'myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),
    # 我收藏的授课讲师
    url(r'myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    # 我收藏的课程
    url(r'myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),
    # 我的消息
    url(r'my_message/$', MyMessageView.as_view(), name="my_message"),

    # 我的发布
    url(r'my_article/$', MyArticleView.as_view(), name="my_article"),

    # 增加发布文章
    url(r'^add_article/$', AddPublishView.as_view(), name="add_article"),

    # 取消发布
    url(r'^delete_article/$', DeleteArticleView.as_view(), name="delete_article"),







]