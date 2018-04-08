from django.shortcuts import render, redirect, Http404, HttpResponse
from django.contrib.auth.decorators import permission_required
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import server, profile, uploadFile
import time, hmac, hashlib, json, socket
from .forms import profileForm, loginForm, userForm, uploadFileForm, downloadFileForm
from django.contrib.auth.models import User
from ast import literal_eval
from .socketConnect import establishContainerConnect, establishRobotConnect, sendRequest
from Robot.settings import CONTAINER_TARGET_SERVER_IP, CONTAINER_TARGET_SERVER_PORT, ROBOT_TARGET_SERVER_IP, \
    ROBOT_TARGET_SERVER_PORT, MEDIA_ROOT, GateOneServer
from django.http import FileResponse
import os

containerSock = establishContainerConnect(CONTAINER_TARGET_SERVER_IP, CONTAINER_TARGET_SERVER_PORT)
robotSock = establishRobotConnect(ROBOT_TARGET_SERVER_IP, ROBOT_TARGET_SERVER_PORT)


# Create your views here.
def hostConnect(request):
    host_ip = request.POST.get('host', None)
    host_user = request.user.username
    host_port = request.POST.get('port', 22)

    if host_port == "": host_port = 22
    print(host_port)
    return render(request, 'gateone.html', {'host_ip': host_ip, 'host_user': host_user, 'host_port': host_port})


# 获取get请求的信息，然后返回gateone的页面

def createSignature(secret, *parts):
    hash = hmac.new(secret, digestmod=hashlib.sha1)
    for part in parts:
        hash.update(part.encode('utf-8'))
    return hash.hexdigest()


def getAuthObj(request):
    # 安装gateone的服务器以及端口.
    gateone_server = GateOneServer
    # 之前生成的api_key 和secret
    secret = 'MzAwNmVkODAwNGJlNDRmYjlkZTIxMDgyZjU2YTMyMDczN'
    api_key = 'MzUxMmRhNTY5YmY5NGNiNWE2ZmJkZGUwODIxY2VlNjYwZ'

    authobj = {
        'api_key': api_key,
        'upn': 'gateone',
        'timestamp': str(int(time.time() * 1000)),
        'signature_method': 'HMAC-SHA1',
        'api_version': '1.0'
    }

    authobj['signature'] = createSignature(secret.encode('utf-8'), authobj['api_key'], authobj['upn'],
                                           authobj['timestamp'])
    auth_info_and_server = {"url": gateone_server, "auth": authobj}
    valid_json_auth_info = json.dumps(auth_info_and_server)
    #   print valid_json_auth_info
    return HttpResponse(valid_json_auth_info)


def createUserRequest(request, serverName):
    _server = server.objects.get(hostName=serverName)
    serverPort = _server.hostPort
    userName = request.user.username
    data = {'createcuser':
                {'port': int(serverPort),
                 'username': userName}}
    jsonData = json.dumps(data)
    try:
        receivingMessage = sendRequest(containerSock, jsonData)
    except socket.timeout:
        return HttpResponse('timeout')
    if receivingMessage['createcuser']['response'] == 'ok':
        _user = request.user
        _serverNum = _user.profile.serverNum
        _serverNum = literal_eval(_serverNum)
        newServers = set(_serverNum)
        newServers.add(serverName)
        _user.profile.serverNum = str(list(newServers))
        _user.save()
        return redirect('/')
    elif receivingMessage['createcuser']['response'] == 'fail':
        return HttpResponse('失败')
    else:
        raise Http404


def deleteUserRequest(request, serverName):
    _server = server.objects.get(hostName=serverName)
    serverPort = _server.hostPort
    userName = request.user.username
    data = {'deletecuser':
                {'port': int(serverPort),
                 'username': '%s' % userName}}
    jsonData = json.dumps(data)
    try:
        receivingMessage = sendRequest(containerSock, jsonData)
    except socket.timeout:
        return HttpResponse('timeout')
    if receivingMessage['deletecuser']['response'] == 'ok':
        _user = request.user
        _serverNum = _user.profile.serverNum
        _serverNum = literal_eval(_serverNum)
        newServers = set(_serverNum)
        newServers.remove(serverName)
        _user.profile.serverNum = str(list(newServers))
        _user.save()
        return redirect('/')
    elif receivingMessage['deletecuser']['response'] == 'fail':
        return HttpResponse('失败')
    else:
        raise Http404


def mainPage(request):
    if request.user.is_authenticated == True:
        return redirect('welcomePage/')
    return render(request, 'index.html')


def register(request):
    logStatus = request.user.is_authenticated
    serverNums = server.objects.all()
    if request.method == 'POST':
        _userForm = userForm(request.POST, instance=request.user)
        if _userForm.is_valid():
            _username = request.POST.get('username')
            _password = request.POST.get('password')
            User.objects.create_user(username=_username, password=_password)
            _user = User.objects.select_related('profile').get(username=_username)
            _user.profile.serverNum = []
            _user.save()
            loginUser = auth.authenticate(username=_username, password=_password)
            if loginUser is not None and loginUser.is_active:
                auth.login(request, loginUser)
            return redirect('/')
    else:
        _userForm = userForm(instance=request.user)
    return render(request, 'register.html',
                  {'userForm': _userForm, 'logStatus': logStatus,
                   'serverNums': serverNums})


def login(request):
    log_status = request.user.is_authenticated
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('/')
            else:
                return render(request, 'loginPage.html',
                              {'form': form, 'password_is_wrong': True, 'logStatus': log_status})
    else:
        form = loginForm()
        return render(request, 'loginPage.html', {'form': form, 'logStatus': log_status})


@login_required(login_url="/login/")
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url="/login/")
def manageAccountServers(request):
    logStatus = request.user.is_authenticated
    serverNums = server.objects.all()
    if request.method == 'POST':
        _profileForm = profileForm(request.POST, instance=request.user.profile)
        if _profileForm.is_valid():
            _serverNum = request.POST.getlist('serverNum')
            _user = request.user
            _user.profile.serverNum = _serverNum
            _user.save()
            return redirect('/')
    else:
        _profileForm = profileForm(instance=request.user.profile)
    return render(request, 'modify.html',
                  {'profileForm': _profileForm, 'logStatus': logStatus,
                   'serverNums': serverNums})


@login_required(login_url="/login/")
def welcomePage(request):
    usingServers = literal_eval(request.user.profile.serverNum)
    print(usingServers)
    tempList = []
    for item in usingServers:
        tempList.append(server.objects.get(hostName=item))
    return render(request, 'welcomePage.html', {'hosts': tempList})


@login_required(login_url="/login/")
def manageServers(request):
    allServers = server.objects.values_list('hostName', flat=True)
    usingServers = literal_eval(request.user.profile.serverNum)
    notUsingServers = list(set(allServers) - set(usingServers))
    return render(request, 'manageServers.html', {'usingHosts': usingServers, 'notUsingHosts': notUsingServers})


@login_required(login_url="/login/")
def connectRobot(request):
    data = {'linkrobot':
                {'username': 'stu'}}
    jsonData = json.dumps(data)
    try:
        receivingMessage = sendRequest(robotSock, jsonData)
    except socket.timeout:
        return HttpResponse('timeout')
    if receivingMessage['linkrobot']['response'] == 'ok':
        robotIP = receivingMessage['linkrobot']['robotip']
        robotPort = receivingMessage['linkrobot']['robotport']
        robotNo = receivingMessage['linkrobot']['robotno']
        print(robotIP, robotPort, robotNo)
        return render(request, 'gateoneRobot.html',
                      {'host_ip': ROBOT_TARGET_SERVER_IP, 'host_user': 'stu', 'host_port': robotPort,
                       'robotNo': robotNo})
    elif receivingMessage['linkrobot']['response'] == 'fail':
        return HttpResponse(receivingMessage['linkrobot']['reason'])
    else:
        raise Http404


@login_required(login_url="/login/")
def disconnectRobot(request, _robotNo):
    data = {'unlinkrobot':
                {'robotno': _robotNo}}
    jsonData = json.dumps(data)
    try:
        receivingMessage = sendRequest(robotSock, jsonData)
    except socket.timeout:
        return HttpResponse('timeout')
    if receivingMessage['unlinkrobot']['response'] == 'ok':
        robotNo = receivingMessage['unlinkrobot']['robotno']
        print(robotNo)
        return HttpResponse('released robot')
    elif receivingMessage['unlinkrobot']['response'] == 'fail':
        return HttpResponse(receivingMessage['unlinkrobot']['reason'])
    else:
        raise Http404


@login_required(login_url="/login/")
def uploadUserFile(request):
    logStatus = request.user.is_authenticated
    usingServers = literal_eval(request.user.profile.serverNum)
    tempList = []
    for item in usingServers:
        tempList.append(server.objects.get(hostName=item))
    if request.method == 'POST':
        _uploadFile = uploadFileForm(request.POST, request.FILES)
        if _uploadFile.is_valid():
            _file = request.FILES.get('uploadFile')
            _targetContainer = request.POST.get('targetContainer')
            userFile = uploadFile(belongTo=request.user, file=_file, targetContainer=_targetContainer)
            userFile.save()

            containerPort = server.objects.get(hostName=_targetContainer).hostPort
            data = {'cupload':
                        {'port': containerPort,
                         'username': request.user.username,
                         'filename': userFile.getFileName()}}
            jsonData = json.dumps(data)
            try:
                receivingMessage = sendRequest(containerSock, jsonData)
            except socket.timeout:
                return HttpResponse('timeout')
            if receivingMessage['cupload']['response'] == 'ok':
                return HttpResponse('success')
            elif receivingMessage['cupload']['response'] == 'failed':
                return HttpResponse('fail')
            else:
                raise Http404
    else:
        _uploadFile = uploadFileForm(request.FILES, request.POST)
    return render(request, 'uploadFilePage.html',
                  {'uploadFileForm': _uploadFile, 'logStatus': logStatus, 'tempList': tempList})


@login_required(login_url="/login/")
def downloadUserFilePage(request):
    logStatus = request.user.is_authenticated
    userFiles = uploadFile.objects.filter(belongTo=request.user)
    usingServers = literal_eval(request.user.profile.serverNum)
    tempList = []
    for item in usingServers:
        tempList.append(server.objects.get(hostName=item))
    if request.method == 'POST':
        _downloadFile = downloadFileForm(request.POST)
        if _downloadFile.is_valid():
            _filename = request.POST.get('filename')
            _targetContainer = request.POST.get('targetContainer')
            containerPort = server.objects.get(hostName=_targetContainer).hostPort

            data = {'cdownload':
                        {'port': containerPort,
                         'username': request.user.username,
                         'filename': _filename}}
            jsonData = json.dumps(data)
            try:
                receivingMessage = sendRequest(containerSock, jsonData)
            except socket.timeout:
                return HttpResponse('timeout')
            if receivingMessage['cdownload']['response'] == 'ok':
                _file = os.path.join(MEDIA_ROOT, 'files', request.user, _filename)
                _targetContainer = request.POST.get('targetContainer')
                userFile = uploadFile()
                userFile.belongTo = request.user
                userFile.file.name = _file
                userFile.targetContainer = _targetContainer
                userFile.save()
                return HttpResponse('success')
            elif receivingMessage['cdownload']['response'] == 'fail':
                return HttpResponse('fail')
            else:
                raise Http404
    else:
        _downloadFile = downloadFileForm(request.POST)
    return render(request, 'downloadFilePage.html',
                  {'downloadFileForm': _downloadFile, 'tempList': tempList, 'userFiles': userFiles,
                   'logStatus': logStatus})


@login_required(login_url="/login/")
def downloadUserFile(request, filePath):
    realFilePath = filePath.replace('+', '/')
    realFilePath = realFilePath.replace('=', ' ')
    filename = realFilePath.split('/')[-1]
    file = open(realFilePath, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s' % filename
    return response
