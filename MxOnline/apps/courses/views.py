from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, CourseResource, Video, CourseCategory, CourseDirection
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


# 课程列表页
class CourseListView(View):
    def get(self, request):
        # 全部课程
        all_courses = Course.objects.all().order_by('-add_time')
        # 热门课程推荐
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        # 选择方向
        all_direction = CourseDirection.objects.all()
        direction_id = request.GET.get('direction', '')
        if direction_id:
            all_courses = all_courses.filter(direction_id=int(direction_id))
            all_category = CourseCategory.objects.filter(direction_id=int(direction_id))
            all_categorys = all_category[0].direction

        category_id = request.GET.get('category', '')
        if category_id:
            all_courses = all_courses.filter(category_id=int(category_id))

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # icontains是包含的意思（不区分大小写）
            # Q可以实现多个字段，之间是or的关系
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    detail__icontains=search_keywords))

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)
        return render(request, "course-list.html", {
            'all_courses': courses,
            'sort': sort,
            'direction_id': direction_id,
            'hot_courses': hot_courses,
            'category_id': category_id,
            'all_category': all_category,
            'all_categorys': all_categorys,
            'all_direction': all_direction,
        })


# 课程搜索
class CourseSearchListView(View):
    def get(self, request):
        # 全部课程
        all_courses = Course.objects.all().order_by('-add_time')
        # all_courses = Course.objects.all()
        # 热门课程推荐
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # icontains是包含的意思（不区分大小写）
            # Q可以实现多个字段，之间是or的关系
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    detail__icontains=search_keywords))
        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)
        return render(request, "course-searchlist.html", {
            'all_courses': courses,
            'sort': sort,

            'hot_courses': hot_courses,

        })


# 课程详情页
class CourseDetailView(View):
    def get(self, request, course_id):
        # 获取对应课程
        course = Course.objects.get(id=int(course_id))
        # 课程的点击数加1
        course.click_nums += 1
        course.save()
        # 课程标签
        # 通过当前标签，查找数据库中的课程
        has_fav_course = False
        has_fav_org = False
        if not request.user.is_authenticated():
            return render(request, "login.html")
        # 必须是用户已登录我们才需要判断是否收藏。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tag

        if tag:
            # 需要从1开始不然会推荐自己
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []
        return render(request, "course-detail.html", {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


# 课程章节详情页面
class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        # 获取课程的学习人数+1
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()

        # 查询用户是否已经学习了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            # 如果没有学习该门课程就关联起来
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 找到学习这门课的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 找到学习这门课的所有用户的id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 通过所有用户的id,找到所有用户学习过的所有过程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        # 通过所有课程的id,找到所有的课程，按点击量去五个
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
        })


# 课程评论
class CommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return render(request, "course-comment.html", {
            'course': course,
            'all_resources': all_resources,
            'all_comments': all_comments,
        })


#添加评论
class AddCommentsView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            # 实例化一个course_comments对象
            course_comments = CourseComments()
            # 获取评论的是哪门课程
            course = Course.objects.get(id = int(course_id))
            # 分别把评论的课程、评论的内容和评论的用户保存到数据库
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')


# 课程章节视频播放页面
class VideoPlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        # 获取课程的学习人数+1
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()

        # 查询用户是否已经学习了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            # 如果没有学习该门课程就关联起来
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 找到学习这门课的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 找到学习这门课的所有用户的id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 通过所有用户的id,找到所有用户学习过的所有过程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        # 通过所有课程的id,找到所有的课程，按点击量去五个
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video,
        })




