#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket


HOST='127.0.0.1'  
PORT=5001
BUFFER_SIZE = 1024




class EElog(object):
    def __init__(self):
        pass
    
    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def disconnect(self):
        self.s.close()
    
    def creatlog(self, logname):
        strsend = 'CREAT:'+logname+'\r\n'
        bytesend = bytes(strsend, encoding = "utf-8")
        self.s.send(bytesend)
        
    def loginfo(self, logcontent):
        strsend = 'LOG:'+logcontent+'\r\n'
        bytesend = bytes(strsend, encoding = "utf-8")
        self.s.send(bytesend)
        
    def closelog(self):
        strsend = 'CLOSE:'
        bytesend = bytes(strsend, encoding = "utf-8")
        self.s.send(bytesend)
    



