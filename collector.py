#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (c) 2016-2017 Christopher Gray & Daniel Phan - Comcast Cable Communications LLC.
# All rights reserved.
# https://github.com/c2theg/DDoS_Infomation_Sharing

from socket import *
import shlex, subprocess
import errno, sys, json, os, time, logging
import argparse
from datetime import datetime
#-----------------------------------------------------------------------------------------------------------------------------------------------------
appTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
appVersion = '0.1.12'
appCurrentPath = os.getcwd()
appCurrentPath.replace("\/",'\\/')

appHeader = """\
     _____ _       _     _           _              _____    __    _____             
    |     | |_ ___|_|___| |_ ___ ___| |_ ___ ___   |     |__|  |  |   __|___ ___ _ _ 
    |   --|   |  _| |_ -|  _| . | . |   | -_|  _|  | | | |  |  |  |  |  |  _| .'| | |
    |_____|_|_|_| |_|___|_| |___|  _|_|_|___|_|    |_|_|_|_____|  |_____|_| |__,|_  |
                                |_|                                             |___|
                                      __     
                                     / _|___ 
                                     > _|_ _|
                                     \_____| 
                                             
                      ___            _     _   ___ _              
                     |   \ __ _ _ _ (_)___| | | _ \ |_  __ _ _ _  
                     | |) / _` | ' \| / -_) | |  _/ ' \/ _` | ' \ 
                     |___/\__,_|_||_|_\___|_| |_| |_||_\__,_|_||_|
                                                                      
                   ___                      _      ___      _    _     
                  / __|___ _ __  __ __ _ __| |_   / __|__ _| |__| |___ 
                 | (__/ _ \ '  \/ _/ _` (_-<  _| | (__/ _` | '_ \ / -_)
                  \___\___/_|_|_\__\__,_/__/\__|  \___\__,_|_.__/_\___|
                       ___                     _    _    ___ 
                      / __|___ _ __  _ __     | |  | |  / __|
                     | (__/ _ \ '  \| '  \ _  | |__| |_| (__ 
                      \___\___/_|_|_|_|_|_(_) |____|____\___|
                                                             
                          ___ __  _  __         ___ __  _ ____ 
                         |_  )  \/ |/ /   ___  |_  )  \/ |__  |
                          / / () | / _ \ |___|  / / () | | / / 
                         /___\__/|_\___/       /___\__/|_|/_/  

"""
print appHeader
print "                  DDoS Source Information Sharing - Syslog Collector"
print "                                    Version ", appVersion
print "            Get Updates from: https://github.com/c2theg/DDoS_Infomation_Sharing \r\n\r\n\r\n"
#-----------------------------------------------------------------------------------------------------------------------------------------------------
#---- Import Config ----- 
try:
    pathConfigFile = appCurrentPath + '/config.json'
    print "Loading config: " + pathConfigFile
    with open(pathConfigFile) as data_file:    
        configData = json.load(data_file)
    varSyslogPort = configData['local']['syslog_port']
    varSyslogProto = configData['local']['syslog_proto']
    
    varDebugging = configData['local']['output_debug']
    varLogFile = configData['local']['log_file']
    varlocal_log_to_file = configData['local']['log_to_file']
    varlocal_syslog_trigger_on = configData['local']['syslog_trigger_on']    
    varSourceCollector = configData['local']['source_collector']
except ValueError:
    print "Error! Could not load the config file: " + pathConfigFile + " \n\n" + sys.exc_info()[0]
    raise
#-----------------------------------------------------------------------
buf = 1500
f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
Local_IP = f.read()

addr = (Local_IP,varSyslogPort)
if varSyslogProto == "udp":
    UDPSock = socket(AF_INET,SOCK_DGRAM) # Create socket and bind to address
    UDPSock.bind(addr)

varAppendText = "\n------------------ DDoS Collector v" + appVersion + " @ " + Local_IP + " READY! (" + appTime + ") Listening on " + str(varSyslogProto) + " " + str(varSyslogPort) + " ------------------\n"
print varAppendText

if varlocal_log_to_file == True:
    with open(varLogFile, "a") as myfile:
        myfile.write(varAppendText)    
        myfile.close
#--------------------- Receive messages -----------------------------------------------------------------------------------------------------
while 1:
    data,addr = UDPSock.recvfrom(buf)
    if not data:
        print ("Client has exited!")
        if varlocal_log_to_file == True:
            with open(varLogFile, "a") as myfile:
                myfile.write("Client has exited!")    
                myfile.close
        break
    else:
        dataStr = str(data)
        print "Received message: ", dataStr
        if dataStr.find(varlocal_syslog_trigger_on) == -1:
            print "Not a valid command or DDoS final command..."
        else:
            varAppendText = "\nValid syslog msg [" + dataStr + "]"
            print varAppendText
            if varlocal_log_to_file == True:
                with open(varLogFile, "a") as myfile:
                    myfile.write(varAppendText)    
                    myfile.close
            # Parse out Alert ID and send it to other process@
            varAlertIDPos = dataStr.index("alert #")
            varRealPos = int(varAlertIDPos + 7)
            varAlertIDLenPos = dataStr.index(", start")
            varAlertID = dataStr[varRealPos:varAlertIDLenPos]
            varAlertID = varAlertID[:10]  # max length 10 chars
            #------------ Start Child Process ----------------------------------
            if '.py' in varSourceCollector:
                varCommand = "python " + appCurrentPath + "/" + varSourceCollector + " " + varAlertID
            else:
                varCommand = "./" + varSourceCollector + " " + varAlertID
                
            print "Spawning New Process -> ",varCommand
#           p = subprocess.Popen("python " + appCurrentPath + "/getSources2.py " + varAlertID, bufsize=-1, shell=True, executable=None, stdin=None, stdout=None, stderr=None)
#           p = subprocess.Popen(varCommand, bufsize=-1, shell=True, executable=None, stdin=None, stdout=None, stderr=None)
            #subprocess.Popen(["rm","-r","some.file"])
            p = subprocess.Popen(varCommand, bufsize=-1, shell=True, executable=None, stdin=None, stdout=None, stderr=None)
UDPSock.close()