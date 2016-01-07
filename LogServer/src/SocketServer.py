#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket, threading, select, wx, time
import globalValues
import EventLog

            
            
def runclientUI(client_sock, client_addr):
    
    app = wx.App()
    # wx.InitAllImageHandlers()
    frame = EventLog.EventLogFrame(client_sock, client_addr)
    app.SetTopWindow(frame)
    
    frame.Show()
    
    app.MainLoop()
    
             
                
if __name__ == '__main__':
    
    HOST='127.0.0.1' 
    PORT=5001
    BUFFER_SIZE = 1024
        
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen(0)
    
    globalValues.gServerRunning = 1
    globalValues.gExitServerFlag = 0
    globalValues.gShutdownServerFlag = 0
    
    print('Server Started!')
    while True:
        
        infds,outfds,errfds = select.select([s,],[],[],5)
        if len(infds) != 0:
            client_sock,client_addr=s.accept()
            print('%s:%s connect' % client_addr) 
            
            #multi-threading for multi-user
            runclientUI(client_sock, client_addr)

      
        
        if globalValues.gExitServerFlag == 1 and globalValues.gServerRunning == 1:

            globalValues.gExitServerFlag = 0    
            globalValues.gShutdownServerFlag = 0
            time.sleep(1)
            break
    

    s.close()
    globalValues.gServerRunning = 0
    print('server stop')
    
        
        
        

        
            
        
        
        







        
    
