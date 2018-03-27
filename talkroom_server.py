#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
聊天室服务器程序v1.0.1
作者：挖洞的土拨鼠
联系：
    GitHub：https://github.com/cisp
    Blog：http://www.cnblogs.com/KevinGeorge/
"""

#引入依赖包、库文件
import sys
import time
import socket
import select
import logging
import datetime


#设置全局配置
reload(sys)
sys.setdefaultencoding("utf-8")
logging.basicConfig(filename="./talkroom.log",level=logging.INFO,filemode='a',format='%(asctime)s-%(levelname)s:%(message)s')


#定义全局变量
test_port = 38080
test_addr = "127.0.0.1"


#定义全局函数
def now():
    return str(datetime.datetime.now())


#定义聊天室类
class TalkRoom(object):
    """创建聊天室类"""
    def __init__(self,ipaddress,port,max):
        """
        构造函数：
            初始化聊天人字典结构
            初始化服务器套接字
            初始化轮询队列
        """
        self.__register_name_dictionary = {}
        self.__server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server.bind((ipaddress,port))
        self.__server.listen(max)#设置聊天室最大限制人数
        self.__readable_socket_list = [self.__server]
        self.__writeable_socket_list = []
        self.__error_socket_list = [self.__server]

    def broadcast(self,sockfd,msg):
        for sock in self.__register_name_dictionary:
            if sock != sockfd:
                try:
                    sock.send("\n"+msg)
                except Exception,reason:
                    logging.info(reason)
                    sock.close()
                    self.broadcast(sock,"[%s %s]已经退出聊天室\n"%(self.__register_name_dictionary[sock][0],now()))
                    self.__register_name_dictionary.pop(sock)

    def running(self):
        while True:
            rs,ws,es = select.select(self.__readable_socket_list,self.__writeable_socket_list,self.__error_socket_list)
            for sockfd in rs:
                if sockfd == self.__server:
                    client,addr = sockfd.accept()
                    self.__register_name_dictionary[client] = (None,addr)
                    client.send("请输入您的昵称:")
                    name = client.recv(1024)
                    self.__register_name_dictionary[client] = (name,addr)
                    self.broadcast(client,"[%s %s]刚刚进入聊天室\n"%(name,now()))
                    self.__readable_socket_list.append(client)
                    self.__error_socket_list.append(client)
                    continue
                else:
                    try:
                        data = sockfd.recv(4096)
                        if data:
                            self.broadcast(sockfd,"[%s %s]"%(self.__register_name_dictionary[sockfd][0],now())+data)
                    except Exception,reason:
                        logging.info(reason)
                        sockfd.close()
                        self.broadcast(sockfd,"[%s %s]已经退出聊天室\n"%(self.__register_name_dictionary[sockfd][0],now()))
                        self.__register_name_dictionary.pop(sockfd)
                        self.__readable_socket_list.remove(sockfd)
                        self.__error_socket_list.remove(sockfd)


if __name__ == "__main__":
    room = TalkRoom(test_addr,test_port,5)
    room.running()
