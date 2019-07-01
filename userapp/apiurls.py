# -*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path
from userapp.api.user import UserListView, UserForgetPassword,\
UserResetPassword, ProfileListView, UpdateUserView, UserChangepassword
from rest_framework.urlpatterns import format_suffix_patterns

# from userapp.api.staticpage import StaticPageView

app_name = 'userapp'

urlpatterns = [
	path('users', UserListView.as_view(), name='user-list'),
	path('users/forgetpassword',UserForgetPassword.as_view()),
	path('users/resetpassword',UserResetPassword.as_view()),
	path('users/changepassword',UserChangepassword.as_view()),
	path('profile', ProfileListView.as_view()),
	path('profile/update',UpdateUserView.as_view()),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)
