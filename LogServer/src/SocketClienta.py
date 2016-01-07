#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import time

# IPV4 TCP connection

HOST='127.0.0.1'  

PORT=5001

BUFFER_SIZE = 1024


        
    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))


s.send('create:RY11111\r\n')



s.send('log:here is log a try for logging server\r\n')

for i in range(11000):
    temp = ('log: This is line: %d\r\n' % i)
    # for Python3
#   strsend = bytes(temp, encoding = "utf-8")
    # for Python2
    strsend = temp 
    s.send(strsend)
#   if i>1000:
    time.sleep(0.01)
#       
s.send('close:\r\n')

s.send('create:RY22222\r\n')
s.send('log:here is log b try for logging server\r\n')
for i in range(5000):
    temp = ('log: This is line: %d\r\n' % i)
    # for Python3
#   strsend = bytes(temp, encoding = "utf-8")
    # for Python2
    strsend = temp 
    s.send(strsend)
#   if i>1000:
    time.sleep(0.01)
    
s.send('close:\r\n')
s.send('exit:\r\n')
    
# for Python3   
# s.send(bytes('close:\r\n', encoding = "utf-8"))
# for Python2.7
