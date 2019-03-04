# -*- coding: utf-8 -*-
import xlrd
import xadmin

from .models import *
from organization.models import CourseOrg


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'degree', 'learn_times', 'students', 'fav_nums',  'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students', 'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']
    model_icon = 'fa fa-book'
    ordering = ['-click_nums']
    # 设置制度字段
    readonly_fields = ['click_nums']
    # 设置字段是否可以编辑
    list_editable = ['degree', 'desc']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]
    refresh_times = [3, 5]
    style_fields = {"detail": "ueditor"}
    import_excel = True
    #
    # def get_media(self):
    #     media = super(CourseAdmin, self).get_media()
    #     path = self.request.get_full_path()
    #     if "add" in path or 'update' in path:
    #         media.add_js([self.static('js/xadmin.js')])
    #     return media


    def queryset(self):
        # 重载queryset方法，来过滤出我们想要的数据的
        qs = super(CourseAdmin, self).queryset()
        # 只显示is_banner=True的课程
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        # obj实际是一个course对象
        obj = self.new_obj
        # 如果这里不保存，新增课程，统计的课程数会少一个
        obj.save()
        # 确定课程的课程机构存在。
        if obj.course_org is not None:
            # 找到添加的课程的课程机构
            course_org = obj.course_org
            # 课程机构的课程数量等于添加课程后的数量
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    # def post(self, request, *args, **kwargs):
    def post(self, request, *args):
        if 'excel' in request.FILES:
            # pass
            # filename = filename.decode('utf-8')
            wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['excel'].read())
            table = wb.sheets()[0]
            row = table.nrows
            sql_list = []
            org_id_list = []
            for i in range(1, row):
                col = table.row_values(i)
                sql = Course(  # 此处不应该写死，容易导入错误，应能自动识别相关顺序
                    name=col[0],
                    desc=col[1],
                    detail=col[2],
                    degree=col[3],
                    learn_times=col[4],
                    students=col[5],
                    fav_nums=col[6],
                    click_nums=col[7],

                )
                sql_list.append(sql)
                # org_id_list.append(col[10])
            Course.objects.bulk_create(sql_list)
            # 更新excel文件中机构包含的课程数
            for id in org_id_list:
                org = CourseOrg.objects.get(id=int(id))
                org_course_nums = org.course_set.all().count()
                org.course_nums = org_course_nums
                org.save()
            # 调用父类的post
        return super(CourseAdmin, self).post(request, args)


class BannerCourseAdmin(object):
    list_display = ['name', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


class CourseDirectionAdmin(object):
    list_display = ['course_direction']
    search_fields = ['course_direction']
    list_filter = ['course_direction']


class CourseCategoryAdmin(object):
    list_display = ['course_category']
    search_fields = ['course_category']
    list_filter = ['course_category']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseDirection, CourseDirectionAdmin)
xadmin.site.register(CourseCategory, CourseCategoryAdmin)



