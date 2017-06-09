#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (c) 2016-2017 Christopher Gray & Daniel Phan - Comcast Cable Communications LLC.
# All rights reserved.
# https://github.com/c2theg/DDoS_Infomation_Sharing
import errno, sys, json, os, time, logging, argparse, base64, ssl, re, string
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class HTTP_Classes:
    var_status = "loaded class"
    
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Content-Type': 'application/json',
       'Connection': 'keep-alive'}
    
    def HTTP_GET_rjson(self, resourceURL, Timeout_Dur=90, error_log='', debug=0):
        try:
            if debug == 1: print "HTTP GET for URL: " + str(resourceURL) + "... \n\n"
            HTTP_Response = requests.Session()
            HTTP_Response = requests.request("GET",str(resourceURL), timeout=Timeout_Dur, verify=False)  #  stream=True
            HTTP_ResponseRAW = HTTP_Response.json()
            if debug == 1: print "\n\n Got back: " + str(HTTP_ResponseRAW) + "\n\n"
            return HTTP_ResponseRAW
        except OSError:
            return "Could not fetch HTTP GET. Reason: " +  sys.exc_info()[0]


    def HTTP_POST_rjson(self, resourceURL, Timeout_Dur=90, error_log='', debug=0):
        try:
            if debug == 1: print "HTTP POST for URL: " + str(resourceURL) + "... \n\n"
            HTTP_Response = requests.Session()
            HTTP_Response = requests.post(str(resourceURL), JSON_Payload, headers=self.hdr, timeout=Timeout_Dur, verify=False, stream=True)  
            HTTP_ResponseRAW = HTTP_Response.json()
            if debug == 1: print "\n\n Got back: " + str(HTTP_ResponseRAW) + "\n\n"
            return HTTP_ResponseRAW
        except OSError:
            return "Could not fetch HTTP POST. Reason: " +  sys.exc_info()[0]


    #------------------------------------------------------------------------------------------------------------------------------------------------
    
    def HTTP_GET_SendJson(self, resourceURL, payload, Timeout_Dur=90, error_log='', debug=0):
        try:
            if debug == 1: 
                print "Sending GET data to: " + resourceURL + "\n"
                print json.dumps(payload, indent=4, sort_keys=True, ensure_ascii=False, encoding='latin1')
            
            HTTP_Response = requests.Session()
            JSON_Payload = json.dumps(payload, ensure_ascii=False, encoding='latin1')
            HTTP_Response = requests.get(str(resourceURL), JSON_Payload, headers=self.hdr, timeout=Timeout_Dur, verify=False)
            HTTP_ResponseRAW = HTTP_Response.json()
            if debug == 1: print "\n\n Got back: " + str(HTTP_ResponseRAW) + "\n\n"
            return HTTP_ResponseRAW
        except OSError:
            return "Could not HTTP GET. Reason: " +  sys.exc_info()[0]    
    
    def HTTP_POST_SendJson(self, resourceURL, payload, Timeout_Dur=90, error_log='', debug=0):
        try:      
            if debug == 1:
                print "Sending POST data to: " + resourceURL + "\n"
                print json.dumps(payload, indent=4, sort_keys=True, ensure_ascii=False, encoding='latin1')
            
            HTTP_Response = requests.Session()
            JSON_Payload = json.dumps(payload, ensure_ascii=False, encoding='latin1')
            HTTP_Response = requests.post(str(resourceURL), JSON_Payload, headers=self.hdr, timeout=Timeout_Dur, verify=False)  #  stream=True
            HTTP_ResponseRAW = HTTP_Response.json()
            if debug == 1: print "\n\n Got back: " + str(HTTP_ResponseRAW) + "\n\n"
            return HTTP_ResponseRAW
        except OSError:
            return "Could not POST HTTP Send. Reason: " +  sys.exc_info()[0]        
       