#!/usr/bin/env python
# -*- coding: utf-8 -*-

#global.py

# server side values
gServerRunning = 0
gExitServerFlag = 0 # for normal exit server, will wait all threading finish
gShutdownServerFlag = 0 # for force shutdown server, will not wait all threading finihed

#client side values
gFilePath = 'D:\\Temp'