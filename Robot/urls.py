"""Robot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import rsm.views as rsmView

urlpatterns = [
    # 管理后台
    path('admin/', admin.site.urls),
    # 首页
    path('', rsmView.mainPage),
    # 建立SSH连接
    path('hostConnect/', rsmView.hostConnect, name='hostConnect'),
    # 建立SSH连接相关——创建签名
    path('createSignature/', rsmView.createSignature, name='createSignature'),
    # 建立SSH连接相关——验证连接合法性
    path('getAuthObj/', rsmView.getAuthObj, name='getAuthObj'),
    # 虚拟机器人创建用户
    path('createUserRequest/<str:serverName>/', rsmView.createUserRequest, name='createUserRequest'),
    # 虚拟机器人删除用户
    path('deleteUserRequest/<str:serverName>/', rsmView.deleteUserRequest, name='deleteUserRequest'),
    # 登录
    path('login/', rsmView.login, name='login'),
    # 注册
    path('register/', rsmView.register, name='register'),
    # 修改用户使用的服务器（测试用方法，正式不使用）
    path('modify/', rsmView.manageAccountServers, name='modify'),
    # 连接虚拟机器人主页
    path('robotPage/', rsmView.robotPage, name='welcomePage'),
    # 用户管理虚拟机器人主页
    path('manageServers/', rsmView.manageServers, name='manageServers'),
    # 连接实体机器人
    path('connectRobot/', rsmView.connectRobot, name='connectRobot'),
    # 断开实体机器人连接
    path('disconnectRobot/<int:_robotNo>', rsmView.disconnectRobot, name='disconnectRobot'),
    # 实体机器人上传文件
    path('RUploadFile/', rsmView.RUploadUserFile, name='RUploadFile'),
    # 实体机器人下载文件
    path('RDownloadFile/', rsmView.RDownloadUserFilePage, name='RDownloadFilePage'),
    # 虚拟机器人上传文件
    path('uploadFile/', rsmView.uploadUserFile, name='uploadFile'),
    # 虚拟机器人下载文件
    path('downloadFile/', rsmView.downloadUserFilePage, name='downloadFilePage'),
    # 下载文件方法
    path('downloadFile/<str:filePath>', rsmView.downloadUserFile, name='downloadFile'),
    # 登出
    path('logout/', rsmView.logout, name='logout'),
    # 批量控制
    path('makeControl/', rsmView.makeControl, name='makeControl'),
    # 连接虚拟机器人
    path('connectContainer/<str:serverName>/', rsmView.connectContainer, name='connectContainer'),
    # 断开虚拟机器人连接
    path('disconnectContainer/<str:serverName>/', rsmView.disconnectContainer, name='disconnectContainer'),
    # 连接仿真终端
    path('connectVNC/<str:serverName>/', rsmView.connectVNC, name='connectVNC'),
    # 断开仿真终端
    path('disconnectVNC/<str:serverName>/', rsmView.disconnectVNC, name='disconnectVNC'),

]
