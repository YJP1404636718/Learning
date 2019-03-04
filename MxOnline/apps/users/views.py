import json
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse


from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm, AddArticleForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course, CourseDirection, CourseCategory
from commucation.models import Article, Keywords
from .models import Banner


#导入serializers
from django.http import JsonResponse
from django.core import serializers

# 二级联动View函数
class SelectView(LoginRequiredMixin, View):
    def get(self, request):
        # 通过get得到父级选择项
        direction_id = request.GET.get('module', '')
        # 筛选出符合父级要求的所有子级，因为输出的是一个集合，需要将数据序列化 serializers.serialize（）
        category = serializers.serialize("json", Course.objects.filter(direction_id=int(direction_id)))
        # 判断是否存在，输出
        if category:
            return JsonResponse({'category': category})


#邮箱和用户名都可以登录
# 基础ModelBackend类，因为它有authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 激活用户
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


# 用户注册
class RegisterView(View):
    # 获取表单信息
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            # 如果用户已存在，则提示错误信息
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get("password", "")
            # 实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            # 写入欢迎信息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册"
            user_message.save()
            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


# 用户注销
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


# 用户登录
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {"msg": "用户名或密码错误！"})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                if user.is_active:
                    # 只有注册激活才能登录
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, "login.html", {"msg": "用户名或密码错误！"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})
        else:
            return render(request, "login.html", {"login_form": login_form})


# 忘记密码
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


# 重置密码
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")

        return render(request, "login.html")


# 修改密码
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


# 用户修改个人信息
class UserinfoView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = "myuser"
        return render(request, 'usercenter-info.html', locals())

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


# 用户图像修改
class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        #上传的文件都在request.FILES里面获取，所以这里要多传一个这个参数
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


# 个人中心修改用户密码
class UpdatePwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',  content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # return HttpResponse('{"status":"fail","msg":"密码错误"}', content_type='application/json')
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


# 发送邮箱修改验证码
class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type='application/json')


# 修改邮箱
class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')


# 我的课程
class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        current_page = "mycourse"
        return render(request, "usercenter-mycourse.html", {
            "user_courses": user_courses,
            "current_page": current_page,
        })


# 我收藏的课程机构
class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象
        for fav_org in fav_orgs:
            # 取出fav_id也就是机构的id。
            org_id = fav_org.fav_id
            # 获取这个机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        current_page = "myfavorg"
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
            "current_page": current_page,
        })


class MyArticleView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = "my_article"
        article_list = Article.objects.filter(user=request.user)

        return render(request, "usercenter-article.html", {
            "current_page": current_page,
            "article_list": article_list,
        })

class DeleteArticleView(View):
    def post(self, request):
        article_id = request.POST.get('article_id', 0)
        article = Article.objects.filter(id=int(article_id))
        article.delete()
        return HttpResponse('{"status":"success"}', content_type='application/json')



# 我收藏的课程机构教师
class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象
        for fav_teacher in fav_teachers:
            # 取出fav_id也就是机构的id。
            teacher_id = fav_teacher.fav_id
            # 获取这个机构对象
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        current_page = "myfavorg"
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
            "current_page": current_page
        })


# 我收藏的课程
class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        current_page = "myfavorg"
        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,
            "current_page": current_page,
        })


# 我的消息
class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)
        # 用戶進入個人頁面清空未讀消息
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 4,request=request)
        messages = p.page(page)
        current_page = "mymessage"
        return render(request, "usercenter-message.html", {
            "messages": messages,
            "current_page": current_page,
        })





class AddPublishView(View):
    def get(self, request):
        return render(request, "usercenter-addarticle.html", {
        })
    def post(self, request):
        article_form = AddArticleForm(request.POST)
        if article_form.is_valid():
            article = Article()
            article.user_id = request.user.id
            article.title = article_form.cleaned_data["title"]
            article.desc = article_form.cleaned_data["desc"]
            # article.tag = article_form.data["tag[]"]
            article.content = article_form.cleaned_data["content"]
            print(article.title,article.desc)
            all_word = Keywords.objects.all()
            for i in all_word:
                if i.word in article.content:
                    return HttpResponse('{"status":"exists", "msg":"存在违禁词"}', content_type='application/json')
            article.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')









# 首页
class IndexView(View):
    def get(self, request):
        #轮播图
        all_banners = Banner.objects.all().order_by('index')
        #课程
        courses = Course.objects.filter(is_banner=False)[:10]
        print(courses)
        #轮播课程
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        #课程机构
        course_orgs = CourseOrg.objects.all()[:15]
        all_direction = CourseDirection.objects.all()
        return render(request, 'indexs.html', {
            'all_banners': all_banners,
            'all_direction': all_direction,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


def pag_not_found(request):
    from django.shortcuts import render_to_response
    # 全局404处理函数
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response