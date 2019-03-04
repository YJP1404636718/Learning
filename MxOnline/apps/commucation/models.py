from django.db import models
from users.models import UserProfile
from datetime import datetime

from DjangoUeditor.models import UEditorField


# # 标签
# class Tag(models.Model):
#     name = models.CharField(max_length=30, verbose_name='标签名称')
#
#     class Meta:
#         verbose_name = '标签'
#         verbose_name_plural = verbose_name
#         ordering = ['id']
#
#     def __str__(self):
#         return self.name



# 文章模型
class Article(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, editable=False, null=True, verbose_name=u"用户", blank=True)
    # user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=200, verbose_name='文章描述')
    content = models.TextField(verbose_name=u'文章内容', blank=True, null=True, max_length=100000)
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    # tag = models.ManyToManyField(Tag, verbose_name='标签')

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name
        # ordering = ['-date_publish']

    def __str__(self):
        return self.title


# 评论模型
class Comment(models.Model):
    content = models.TextField(blank=True, null=True,verbose_name='评论内容')
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户名')
    # email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮箱地址')
    # url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    date_publish = models.DateTimeField(verbose_name='发布时间', default=datetime.now)
    user = models.ForeignKey(UserProfile, blank=True, null=True, verbose_name='用户', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章', on_delete=models.CASCADE)
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        # ordering = ['-date_publish']
    #
    # def __str__(self):
    #     return str(self.id)


class Keywords(models.Model):
    word = models.CharField(max_length=30, verbose_name='违禁关键字')

    class Meta:
        verbose_name = '违禁关键字'
        verbose_name_plural = verbose_name
