from django.shortcuts import render, redirect, Http404, HttpResponse
from django.contrib.auth.decorators import permission_required
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import server, profile
import time, hmac, hashlib, json, socket
from .forms import profileForm, loginForm, userForm
from django.contrib.auth.models import User
from ast import literal_eval


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
    gateone_server = 'https://127.0.0.1'
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
    def sendRequest(ip, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((ip, port))
        print(message.encode('utf-8'))
        sock.sendall(message.encode('utf-8'))
        sock.close()

    _server = server.objects.get(hostName=serverName)
    serverIP = _server.hostIP
    serverPort = _server.hostPort
    userName = request.user.username
    port = 48000
    data = {'createcuser':
                {'port': int(serverPort),
                 'username': userName}}
    jsonData = json.dumps(data)
    # sendRequest(serverIP, port, jsonData)
    _user = request.user
    _serverNum = _user.profile.serverNum
    _serverNum = literal_eval(_serverNum)
    newServers = set(_serverNum)
    newServers.add(serverName)
    _user.profile.serverNum = str(list(newServers))
    _user.save()
    return redirect('/')


def deleteUserRequest(request, serverName):
    def sendRequest(ip, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((ip, port))
        print(message.encode('utf-8'))
        sock.sendall(message.encode('utf-8'))
        sock.close()

    _server = server.objects.get(hostName=serverName)
    serverIP = _server.hostIP
    serverPort = _server.hostPort
    userName = request.user.username
    port = 48000
    data = {'deletecuser':
                {'port': '%s' % serverPort,
                 'username': '%s' % userName}}
    jsonData = json.dumps(data)
    # sendRequest(serverIP, port, jsonData)
    _user = request.user
    _serverNum = _user.profile.serverNum
    _serverNum = literal_eval(_serverNum)
    newServers = set(_serverNum)
    newServers.remove(serverName)
    _user.profile.serverNum = str(list(newServers))
    _user.save()
    return redirect('/')


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
    def sendRequest(ip, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((ip, port))
        print(message.encode('utf-8'))
        sock.sendall(message.encode('utf-8'))
        receivingMessage = sock.recv(1024)
        print(receivingMessage)
        sock.close()

    serverIP = '222.200.177.38'
    port = 48100
    data = {'linkrobot':
                {'username': 'stu'}}
    jsonData = json.dumps(data)
    sendRequest(serverIP, port, jsonData)
    return redirect('/')
