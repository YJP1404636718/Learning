# -*- coding:utf-8 -*-
from django import forms


class CommentForm(forms.Form):
    '''
    评论表单
    '''
    author = forms.CharField(widget=forms.HiddenInput(attrs={"id":"author"}))
    comment = forms.CharField(widget=forms.Textarea(attrs={"id":"comment","class": "message_input",
                                                           "required": "required", "cols": "25",
                                                           "rows": "5", "tabindex": "4"}),
                                                    error_messages={"required":"评论不能为空",})
    article = forms.CharField(widget=forms.HiddenInput(attrs={"id":"article"}))

#
#
# class CommentForm(forms.Form):
#     '''
#     评论表单
#     '''
#     author = forms.CharField(required=True)
#
#     comment = forms.CharField(required=True)
#
#     article = forms.CharField(required=True,cols=25)


