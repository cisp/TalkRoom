#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
聊天室客户端程序v1.0.1
作者：挖洞的土拨鼠
联系：
    GitHub：https://github.com/cisp
    Blog：http://www.cnblogs.com/KevinGeorge/
"""

#引入依赖包、库文件
import sys
import time
import select
import socket
import logging
import datetime

#设置全局配置
reload(sys)
sys.setdefaultencoding("utf-8")
logging.basicConfig(filename="./talkclient.log",level=logging.INFO,filemode='a',format='%(asctime)s-%(levelname)s:%(message)s')


#定义全局变量
test_port = 38080
test_addr = "127.0.0.1"


#定义全局函数
def now():
    return str(datetime.datetime.now())

def inputflag() :
    sys.stdout.write('[MySelf %s]'%now())
    sys.stdout.flush()


#定义客户端类
class TalkClient(object):
    def __init__(self,ipaddress,port):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__readable_socket_list = [sys.stdin,self.__client]
        self.__writeable_socket_list = []
        self.__error_socket_list = [self.__client]
        try:
            self.__client.connect(("127.0.0.1", 38080))
        except Exception,reason:
            logging.info(reason)
            exit(0)
        print "[MySelf %s]刚刚进入聊天室"%now()
        banner = self.__client.recv(1024)
        print banner
        name =raw_input()
        self.__client.send(name)
        inputflag()

    def running(self):
        while True:
            rs,ws,es = select.select(self.__readable_socket_list,self.__writeable_socket_list,self.__error_socket_list)
            for sockfd in rs:
                if sockfd == self.__client:
                    data = self.__client.recv(4096)
                    if data:
                        sys.stdout.write(data)
                        inputflag()
                    else:
                        exit(0)
                else:
                    message = sys.stdin.readline()
                    self.__client.send(message)
                    inputflag()



#主程序入口
if __name__ == "__main__":
    client = TalkClient(test_addr,test_port)
    client.running()
