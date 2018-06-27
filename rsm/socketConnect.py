import socket
import json


# 该文件用于定义建立TCP连接，发送消息的方法

# 建立TCP连接
def establishContainerConnect(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置5秒超时
    sock.settimeout(5.0)
    sock.connect((ip, port))
    return sock


# 建立TCP连接
def establishRobotConnect(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置5秒超时
    sock.settimeout(5.0)
    sock.connect((ip, port))
    return sock


# 发送消息方法
def sendRequest(sock, message):
    sock.sendall(message.encode('utf-8'))
    print(message)
    # 获取完整的消息
    receivingMessage = sock.recv(1024)
    print(receivingMessage)
    # 消息前端有消息长度，找到消息正式开始的位置
    startPos = receivingMessage.find(b'{')
    # 获取长度
    receivingMessageLength = int(receivingMessage[:startPos].decode('utf-8'))
    # 获取消息部分
    receivingMessage = receivingMessage[startPos:startPos + receivingMessageLength]
    print(receivingMessage)
    # 解析json内容
    receivingMessage = json.loads(receivingMessage.decode('utf-8'))
    print(receivingMessage)
    return receivingMessage
