# -*- coding: utf-8 -*-
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile
from commucation.models import Article
from DjangoUeditor.models import UEditorField



class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # incalid
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    '''用户更改图像'''
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    '''个人中心信息修改'''
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']


class AddArticleForm(forms.Form):
    title = forms.CharField(required=True)
    desc = forms.CharField(required=True)
    content = forms.CharField(required=True)

# class AddArticleForm(forms.Form):
#     title = forms.CharField(required=True)
#     desc = forms.CharField(required=True)
#     content = UEditorField(width=800, height=300, toolbars="full",imagePath="commucation/ueditor",
#                           filePath="commucation/ueditor", default='')






    # tag = forms.CharField(required=None)
    # date_publish = forms.DateTimeField(required=True)
    # password2 = forms.CharField(required=True, min_length=5)
    # class Meta:
    #     model = Article
    #     fields = ['title', 'desc', 'content', 'date_publish']