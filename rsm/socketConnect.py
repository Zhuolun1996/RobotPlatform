import socket
import json


def establishContainerConnect(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    sock.connect((ip, port))
    return sock

def establishRobotConnect(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    sock.connect((ip, port))
    return sock

def sendRequest(sock,message):
    sock.sendall(message.encode('utf-8'))
    print(message)
    receivingMessage = sock.recv(1024)
    print(receivingMessage)
    startPos=receivingMessage.find(b'{')
    receivingMessageLength=int(receivingMessage[:startPos].decode('utf-8'))
    receivingMessage=receivingMessage[startPos:startPos+receivingMessageLength]
    print(receivingMessage)
    receivingMessage = json.loads(receivingMessage.decode('utf-8'))
    print(receivingMessage)
    return receivingMessage