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
    path('admin/', admin.site.urls),
    path('', rsmView.mainPage),
    path('hostConnect/', rsmView.hostConnect, name='hostConnect'),
    path('createSignature/', rsmView.createSignature, name='createSignature'),
    path('getAuthObj/', rsmView.getAuthObj, name='getAuthObj'),
    path('createUserRequest/<str:serverName>/', rsmView.createUserRequest, name='createUserRequest'),
    path('deleteUserRequest/<str:serverName>/', rsmView.deleteUserRequest, name='deleteUserRequest'),
    path('login/', rsmView.login, name='login'),
    path('register/', rsmView.register, name='register'),
    path('modify/', rsmView.manageAccountServers, name='modify'),
    path('welcomePage/', rsmView.welcomePage, name='welcomePage'),
    path('manageServers/', rsmView.manageServers, name='manageServers'),
    path('connectRobot/', rsmView.connectRobot, name='connectRobot'),
    path('disconnectRobot/<int:_robotNo>', rsmView.disconnectRobot, name='disconnectRobot'),
    path('uploadFile/', rsmView.uploadUserFile, name='uploadFile'),
    path('downloadFile/', rsmView.downloadUserFilePage, name='downloadFilePage'),
    path('downloadFile/<str:filePath>', rsmView.downloadUserFile, name='downloadFile'),

]
