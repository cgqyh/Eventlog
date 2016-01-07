#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import globalValues
import os
import Queue

import wx
import wx.lib.newevent
import threading, time

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade
BUFFER_SIZE = 1024
LogUpdateEvent, EVT_LOG_UPDATE = wx.lib.newevent.NewEvent()   
LogClearEvent, EVT_LOG_CLEAR = wx.lib.newevent.NewEvent()   


class EventLog(object):
    
    
    def __init__(self):
        
        self.file_open_flag = 0

    def CreateLog(self, filename):
        
        s = datetime.now()
        now = s.strftime('%d%b%Y_%H%M%S')
        self.f = open('%s\\%s_%s.log' % (globalValues.gFilePath, filename, now), 'w')
            
        self.file_open_flag = 1  #mark file opened
        
    def Logging(self, log_content):
        if self.file_open_flag == 1:
            self.f.write(log_content)
            self.f.flush()
            os.fsync(self.f)
        
    
    def CloseLog(self):
        self.file_open_flag = 0
        self.f.close()
        
    
           
class EventLogFrame(wx.Frame):
#     def __init__(self, *args, **kwds):
    def __init__(self, client_sock, client_addr):
        


        # begin wxGlade: EventLogFrame.__init__
#         wx.Frame.__init__(self, *args, **kwds)
        wx.Frame.__init__(self, None, -1, "")
        self.button_1 = wx.Button(self, wx.ID_ANY, ("Save Log"))
        self.list_box_1 = wx.ListBox(self, wx.ID_ANY, choices=[], style = wx.LB_HSCROLL)

        self.__set_properties()
        self.__do_layout()
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.DclickList, self.list_box_1)
        self.Bind(wx.EVT_BUTTON, self.OnSave, self.button_1)
        
        #custom event
        self.Bind(EVT_LOG_UPDATE, self.OnaddLog)
        self.Bind(EVT_LOG_CLEAR, self.OnLogClear)        
        
        
        self.client_sock = client_sock
        self.client_addr = client_addr
        
        self.isthreadrunning = 0    # for timmer event
        self.isrolling = 1          # for list control rolling
        self.issavelog = 0          # for save log during logging
        self.timer.Start(1000)
        
        
        
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: EventLogFrame.__set_properties
        self.SetTitle("EventLog GUI")
        self.SetSize((650, 350))
        self.SetBackgroundColour(wx.Colour(232, 232, 232))

        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: EventLogFrame.__do_layout
        grid_sizer_1 = wx.FlexGridSizer(2, 1, 0, 0)
        grid_sizer_1.Add(self.button_1, 0, 0, 0)
        grid_sizer_1.Add(self.list_box_1, 0, wx.EXPAND, 0)
        self.SetSizer(grid_sizer_1)
#         grid_sizer_1.Fit(grid_sizer_1)
        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableCol(0)
        self.Layout()
        # end wxGlade
        
    def OnTimer(self, event):
        if self.isthreadrunning == 0:
            self.q = Queue.Queue(0)
            self.t = threading.Thread(target = self.run_client_socket, args = (self.client_sock, self.client_addr))
            self.isthreadrunning = 1
            self.t.start()   
            
        elif self.isthreadrunning == 1:    #running
            pass
        elif self.isthreadrunning == 2:
            self.OnQuit()
            
            
    def DclickList(self, event):  # wxGlade: EventLogFrame.<event_handler>
        if self.isrolling == 0:
            self.isrolling = 1
        else:
            self.isrolling = 0
        event.Skip()

    def OnSave(self, event):  # wxGlade: MyFrame.<event_handler>
        self.issavelog = 1
        event.Skip()
        
    def OnaddLog(self, event):
        if self.q.empty()==False:
            temp = self.q.get()
            self.__addLog(temp)
        event.Skip()
    
                 
    def __addLog(self, log):
        
        self.list_box_1.Append(log)
        n = self.list_box_1.GetCount()
        
        if self.isrolling == 1:
            if n>10000:
                self.list_box_1.Delete(0)
                self.list_box_1.SetSelection(n-2)
            else:
                self.list_box_1.SetSelection(n-1)
            

    
    def OnLogClear(self, event):
        self.__clearLog()
        event.Skip()
        
    def __clearLog(self):
        self.list_box_1.Clear()

        
    def OnQuit(self):
        wx.CallAfter(self.__quit)
        
        
    def __quit(self):
        self.Close(True)
        self.isthreadrunning = 0
        


    def run_client_socket(self, client_sock, client_addr):
        
        mybuffer = ''
        temp = ''
        logging_flag = 0 # mark whether is logging started
        
        isrunning=1     # 1 means socket running
                        # have to use different value to avoid conflict with Timmer event
                        # using self.isthreadrunning will have risk if log out is not done 
        while True:
            temp = client_sock.recv(BUFFER_SIZE)
            
            # for Python3
    #         buffer = buffer + str(temp, encoding = "utf-8")
            # for Python2
            mybuffer = mybuffer + temp
                   
            while mybuffer.find('\r\n')>=0:
                
                command = mybuffer[0:mybuffer.find(':')]
                command = command.upper()
                
                content = mybuffer[mybuffer.find(':')+1:mybuffer.find('\r\n')].lstrip() 
                
                mybuffer = mybuffer[mybuffer.find('\r\n')+2:]

                
                if globalValues.gShutdownServerFlag ==0:
                    if command == 'CREATE' and logging_flag == 0:
                        log = EventLog()
                        log.CreateLog(content)
                        filename = content
                        logging_flag = 1
                        
                        evt = LogClearEvent()
                        wx.PostEvent(self, evt)

    
                    elif command == 'CREATE' and logging_flag == 1:
                        pass
                                            
                    elif command == 'LOG' and logging_flag == 1:
                        stime = datetime.now()
                        now = stime.strftime('%H:%M:%S: ')  
                        log.Logging(now + content+'\n')
                        
#                         self.addLog(now+content+'\r\n')

                        
                        self.q.put(now + content+'\r\n')

                        # use event to display on UI to avoid conflict
                        evt = LogUpdateEvent()
                        wx.PostEvent(self, evt)
                        
                    elif command == 'LOG' and logging_flag == 0:
                        pass
             
                                      
                    elif command == 'CLOSE':
                        if logging_flag == 1: 
                            log.CloseLog()
                            logging_flag = 0
                        time.sleep(0.5)
                        

                    elif command == 'EXIT':
                        if logging_flag == 1:
                            log.CloseLog()
                            logging_flag = 0
                        isrunning = 0
                        #considering mulit-client situation
                        #no needed here
                        globalValues.gExitServerFlag = 1
                        globalValues.gShutdownServerFlag = 1
                        break                        
                    
                            
             
                # Server shutdown by other threading  
                else:   # SHUTDOWN command may send by other threading
                # exit server directly
                    if logging_flag == 1:
                        log.CloseLog()
                        logging_flag = 0  
                    if isrunning == 1:  
                        isrunning = 0
                    
                if self.issavelog == 1:
                    pos = mybuffer.find('\r\n')
                    addcontent = 'CLOSE:\r\n'+'CREATE:'+filename+'\r\n'
                    mybuffer = mybuffer[0:pos+2]+ addcontent + mybuffer[pos+2:]
                    self.issavelog = 0
                     
                
                
            if isrunning == 0:
                break
        self.isthreadrunning = 2
        print('quit socket')


        
    
