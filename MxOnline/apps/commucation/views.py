from django.shortcuts import render
from commucation.models import Article, Comment, Keywords
from django.views.generic import View
from commucation.forms import *
from django.http import HttpResponse
from django.db.models import Q


class ContentListView(View):
    def get(self, request):
        all_comments = Article.objects.all()
        article_lists = Article.objects.filter().order_by('?')[:14]
        articles = article_lists[:3]
        # 推荐排行
        recommend_lists = Article.objects.filter(is_recommend=True).order_by('?')[:2]

        # 浏览排行
        click_lists = all_comments.order_by("-click_count")[:3]

        return render(request, "commucation-list.html", locals())


class ArticleListView(View):
    def get(self, request):
        # 获取文章id
        id = request.GET.get('id', None)
        article = Article.objects.get(pk=id)
        article.click_count += 1
        article.save()
        all_comments = Article.objects.all()
        # 推荐排行
        recommend_lists = Article.objects.filter(is_recommend=True).order_by('?')[:2]

        # 浏览排行
        click_lists = all_comments.order_by("-click_count")[:3]
        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    # 'url': request.user.url,
                                    # is_authenticated()判断用户是否登录
                                    'article': id} if request.user.is_authenticated() else {'article': id})



        comments = Comment.objects.filter(article=article).order_by('id')

        comment_list = []
        for comment in comments:
            for item in comment_list:
                # hasattr() 函数用于判断对 象是否包含对应的属性。
                if not hasattr(item, 'children_comment'):
                    # setattr 函数对应函数 getatt()，用于设置属性值，该属性必须存在。
                    setattr(item, 'children_comment', [])

                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
        return render(request, "commucation-article.html", locals())


# 提交评论
class commentView(View):
    def post(self, request):
        comment_form = CommentForm(request.POST)
        # 获取表单信息
        if comment_form.is_valid():
            comment = Comment()
            comment.username = comment_form.cleaned_data["author"]
            comment.content = comment_form.cleaned_data["comment"]
            all_word = Keywords.objects.all()
            for i in all_word:
                if i.word in comment.content:
                    print("存在违禁词")
                    return HttpResponse('{"status":"exists", "msg":"存在违禁词"}', content_type='application/json')
            comment.user = request.user
            comment.article_id = comment_form.cleaned_data["article"]
            comment.save()
            all_comment = Comment.objects.all()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')
