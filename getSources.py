#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (c) 2016-2017 Christopher Gray & Daniel Phan - Comcast Cable Communications LLC.
# All rights reserved.
# https://github.com/c2theg/DDoS_Infomation_Sharing

#--- Force Python2 as Suds doesn't support Python3 fully as of 11/10/2016
#This product includes GeoLite2 data created by MaxMind, available from http://www.maxmind.com
#Inital: 12/23/16  Updated: 2/5/17
from socket import *
from io import StringIO
from datetime import datetime
import errno, sys, json, os, time, logging, urllib, argparse, base64, ssl, re, string
import requests
import urllib2
#from sslcontext import create_ssl_context, HTTPSTransport

# Uncomment to disable SSL verification - Careful! This could compromise your ArborSP zone_secret
#ssl._create_default_https_context = ssl._create_unverified_context

#------- Suds ------- 
# - https://pypi.python.org/pypi/suds 
# - https://jortel.fedorapeople.org/suds/doc/suds.options.Options-class.html
# - https://bitbucket.org/jurko/suds

import suds
import suds.client

#logging.basicConfig(level=logging.INFO)
#from suds.client import Client
#logging.getLogger('suds.client').setLevel(logging.DEBUG)

#------ MaxMind Legacy GeoIP API ------  https://github.com/maxmind/GeoIP2-python --- https://github.com/maxmind/geoip-api-python
try:
    import GeoIP
except OSError:
    pass
#------ Variables ------
reload(sys)
sys.setdefaultencoding('utf8')
PythonVer = sys.version_info
appCurrentPath = os.getcwd()
appCurrentPath.replace("\/",'\\/')
appTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
appVersion = '0.2.17'
SourcesFound = 0
OutputDict = []
OutputJSON = ""
SendData = []
#---- Import Config ----- 
try:
    ConfigFilePath = appCurrentPath + '/config.json'
    #print "Loading Config file: ", ConfigFilePath
    with open(ConfigFilePath) as data_file:
        configData = json.load(data_file)
        #----------------------------------------
    #print "Config Data: ", configData
    varArborURL = 'https://' + configData['arbor']['url']
    varArborPort = configData['arbor']['port']
    varArborKey = configData['arbor']['key']
    varArborVersion = configData['arbor']['version']
    varArborUser = configData['arbor']['user']
    varArborPasswd = configData['arbor']['passwd']
    varArborCall = configData['arbor']['call']
    varArborWSDL = 'SDKs/' + str(varArborVersion) + '/' + configData['arbor']['wsdl']
    WSDLfile =  appCurrentPath + "/" + varArborWSDL
    if os.path.isfile(WSDLfile):
        print "WSDL file loaded!"
    else:
        print "WSDL file (", WSDLfile, ") DOES NOT exist! Please download the Arbor SDK and put the WSDL in the correct location under SDKs/<Version>/  and make sure its set correctly in config.json"
        sys.exit(0)
    #--------------------------------------------------------------
    varlocaltimezone = configData['local']['timezone']
    varlocaldebugging = configData['local']['output_debug']
    varLogFile = configData['local']['log_file']
    varlocal_log_to_file = configData['local']['log_to_file']
    varlocal_wait_before_pull = configData['local']['wait_before_pull']
    
    varIdentity_name = configData['identity']['name']
    varIdentity_asn = configData['identity']['asn']
    varIdentity_domain = configData['identity']['domain']
    varIdentity_company_type = configData['identity']['company_type']
    varGeoIPDir = configData['geo']['files_path']
    varRemoteURL = configData['remote']['url']
except ValueError:
    print ("Oops! had a problem with the config file", sys.exc_info()[0])
    sys.exit(0)
#------ GET CLI Input -----------------------------------------------------------
try:
    parser = argparse.ArgumentParser()
    parser.add_argument("echo")
    args = parser.parse_args()
    varArgumentReceieved = args.echo[:10]
    #varArgumentReceieved = int(varArgumentReceieved)
    if varArgumentReceieved is None:
        print "\n\nEnter a Alert ID to lookup \n\n"
        sys.exit(0)
except OSError:
    pass
#-------------- Functions -----------------------------------------------------------------------------------------------
def props(x):
    return dict((key, getattr(x, key)) for key in dir(x) if key not in dir(x.__class__))
#------------------------------------------------------ Code -------------------------------------------------------------
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
print "                   DDoS Source Information Sharing - Data Collector"
print "                                    Version: " + appVersion + "\n\n\n"
print "            Get Updates from: https://github.com/c2theg/DDoS_Infomation_Sharing \r\n\r\n\r\n"

if sys.version_info >= (2,7,9):
    print "You are running an old version of Python. please upgrade it for this application to run"
    sys.exit(0)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    print "Legacy Python " + str(PythonVer) + " doesn't verify HTTPS certificates by default. Forcing override."
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    #ssl._create_default_https_context = _create_unverified_https_context
    ssl._create_default_https_context = ssl._create_unverified_context  #SSL fix for python 2.7.6+

    
    
# Customize these settings:
#sslverify = True
#cafile = None
#capath = None

#kwargs = {}
#sslContext = create_ssl_context(sslverify, cafile, capath)
#kwargs['transport'] = HTTPSTransport(sslContext)

    
hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Content-Type': 'application/json',
       'Connection': 'keep-alive'}
page = ''
#-------------- Get the GeoIP Database file ------------------------------------------------------------------------------
print 'This product includes GeoLite2 data created by MaxMind, available from <a href="http://www.maxmind.com">http://www.maxmind.com</a>.'
if varlocaldebugging == True:
    print "Loading the following Maxmind GeoIP database from path: " + varGeoIPDir + ", GeoLiteCity.dat, GeoLiteCityv6.dat, GeoIPASNum.dat, GeoIPASNumv6.dat \n\n"    
    #-- https://dev.maxmind.com/geoip/legacy/geolite/
try:
    geoip_v4    = GeoIP.open(varGeoIPDir + "GeoLiteCity.dat",   GeoIP.GEOIP_MEMORY_CACHE) #GEOIP_STANDARD
    geoip_v6    = GeoIP.open(varGeoIPDir + "GeoLiteCityv6.dat", GeoIP.GEOIP_MEMORY_CACHE)
    geoipASN_v4 = GeoIP.open(varGeoIPDir + "GeoIPASNum.dat",    GeoIP.GEOIP_MEMORY_CACHE)
    geoipASN_v6 = GeoIP.open(varGeoIPDir + "GeoIPASNumv6.dat",  GeoIP.GEOIP_MEMORY_CACHE)
except OSError:
    print "Could not load GeoIP file(s)! Please run \n"
    sys.exit(0)
#-------------------------------------------------------------------------------------------------------------------------    
print "Waiting " + str(varlocal_wait_before_pull) + " seconds before pulling data from Arbor."
time.sleep(varlocal_wait_before_pull)
#-------------------------------------------------------------------------------------------------------------------------
alertDetailsURL = varArborURL + "/arborws/alerts?api_key=" + varArborKey + "&filter=" + varArgumentReceieved
alertDetailsResponse = requests.Session()
alertDetailsResponse = requests.get(alertDetailsURL, timeout=60, verify=False, stream=True)
alertDetailsResponseRAW = alertDetailsResponse.json()
#print alertDetailsResponseRAW
misuseTypes = ''
for i in alertDetailsResponseRAW:
    misuseTypes += str(i['misuseTypes'])
misuseTypes = misuseTypes[1:]  # [u'TCP SYN']
misuseTypes = misuseTypes[:-1]  # [u'TCP SYN']
misuseTypes = misuseTypes.replace("u'", "")
misuseTypes = misuseTypes.replace("'", "")
#print "Misuse Types: "  + misuseTypes
#--------------------------------------------------------------------------------------------------------------------------
#    mitDetailsURL = varArborURL + "/arborws/mitigations/status?api_key=" + varArborKey + "&filter=" + varArgumentReceieved
#    mitDetailsResponse = requests.Session()
#    mitDetailsResponse = requests.get(mitDetailsURL, timeout=60, verify=False, stream=True)
#    mitDetailsResponseRAW = mitDetailsResponse.json()
#--------------------------------------------------------------------------------------------------------------------------
if varlocaldebugging == True:
    print "Connecting to:",varArborURL," User: ",varArborUser, " WSDL: " + WSDLfile
try:
    t = suds.transport.https.HttpAuthenticated(username=varArborUser, password=varArborPasswd)
    t.handler = urllib2.HTTPDigestAuthHandler(t.pm)
    t.urlopener = urllib2.build_opener(t.handler)
    #client = suds.client.Client(url, **kwargs)
    client = suds.client.Client(url='file:///' + WSDLfile, location=varArborURL + '/soap/sp', transport=t)
    #client = suds.client.Client(url='file:///' + WSDLfile, location=varArborURL + '/soap/sp', transport=t, **kwargs)
    client.set_options(service='PeakflowSPService', port='PeakflowSPPort', cachingpolicy=1) # retxml=false, prettyxml=false   # https://jortel.fedorapeople.org/suds/doc/suds.options.Options-class.html    
    ArborResultRAW = client.service.getDosAlertDetails(varArgumentReceieved)
    #ArborMitResultRAW = client.service.getMitigationStatisticsByIdXML(varArgumentReceieved)
    #print(ArborResultRAW)
except ValueError:
    print "Oops! Could not connect to arbor. " +  sys.exc_info()[0]
    sys.exit(0)
#--------------------------------------------------------------------------------------------------------
try:
    ArborResultJSON = props(ArborResultRAW)
    if varlocal_log_to_file == True:
        varAppendText = str("\nAlert ID: " + varArgumentReceieved + "\n")
        with open(varLogFile, "a") as myfile:
            myfile.write(varAppendText)
            myfile.close
    #--------------------------------------------------------------------
    if 'src_addr' in ArborResultJSON:
        Sources = ArborResultJSON['src_addr']
        TempOutputDict_ALL = {}
        TempOutputDict_ALL['ProviderName'] = varIdentity_name
        TempOutputDict_ALL['ProviderASN'] = varIdentity_asn
        TempOutputDict_ALL['company_type'] = varIdentity_company_type
        for x in Sources:
            if '/32' in x.id:
                if x.net.bps != 0:
                    if x.net.pps != 0:
                        #print "IP Address: ", x.id, "BPS: ", x.net.bps, "PPS: ", x.net.pps
                        SourcesFound += 1
                        TempOutputDict = {}
                        CleanIP = x.id.split("/")[0]                    
                        TempOutputDict['IPaddress'] = CleanIP
                        #---- do GeoIP Lookup ----------
                        #print " (IPv4) "
                        gir = geoip_v4.record_by_addr(CleanIP)
                        if gir is not None:
                            #------------ ASN ---------
                            girASN = geoipASN_v4.org_by_addr(CleanIP)
                            #print "ASN: " + str(girASN)   # AS16509 Amazon.com, Inc.
                            if girASN is not None:
                                try:
                                    ASN_Number = girASN.split(' ', 1)[0] # AS36351
                                    ASN_Number = ASN_Number[2:]
                                    ASN_Name = girASN.split(' ', 1)[1]   # Amazon.com, Inc.
                                    ASN_Name = re.sub('[ ](?=[ ])|[^-_,A-Za-z0-9. ]+', '', ASN_Name)
                                except ValueError:
                                    raise
                            else:
                                ASN_Number = 0
                                ASN_Name = "na"
                            #---------- Generate Output ---------------------------------------------
                            if gir['city'] is not None:
                                TempOutputDict['City'] = str(gir['city']).decode('utf-8', 'ignore')
                            else:
                                TempOutputDict['City'] = "na"
                                
                            if gir['region'] is not None:
                                TempOutputDict['State'] = unicode(gir['region'], "utf-8")
                            else:
                                TempOutputDict['State'] = "na"

                            if gir['country_code'] is not None:
                                TempOutputDict['Country'] = unicode(gir['country_code'], "utf-8")
                            else:
                                TempOutputDict['Country'] = "na"

                            #TempOutputDict['latitude'] = gir['latitude']
                            #TempOutputDict['longitude'] = gir['longitude']
                            TempOutputDict['Extra'] = str(gir['latitude']) + "," + str(gir['longitude'])
                            TempOutputDict['TotalBPS'] = x.net.bps
                            TempOutputDict['TotalPPS'] = x.net.pps
                            TempOutputDict['SourceASN'] = ASN_Number
                            TempOutputDict['SourceASNName'] = ASN_Name 
                            TempOutputDict['AttackType'] = misuseTypes
                            OutputDict.append(TempOutputDict)
                        else:
                            if varlocaldebugging == True:
                                print "GeoIP came back empty for IP: " + CleanIP
                    
                    #--- Clear temp variables ---
                    TempOutputDict = None
                    gir = None
                    girASN = None

            elif '/128' in x.id:
                if x.net.bps != 0:
                    if x.net.pps != 0:
                        #print "IP Address: ", x.id, "BPS: ", x.net.bps, "PPS: ", x.net.pps
                        SourcesFound += 1
                        TempOutputDict = {}
                        CleanIP = x.id.split("/")[0]
                        TempOutputDict['IPaddress'] = CleanIP
                        #---- do GeoIP Lookup ----------  
                        #print " (IPv6) "
                        gir = geoip_v6.record_by_addr(CleanIP)
                        if gir is not None:
                            #------------ ASN ---------
                            girASN = geoipASN_v6.org_by_addr(CleanIP)
                            #print "ASN: " + str(girASN)   # AS16509 Amazon.com, Inc.
                            if girASN is not None:
                                try:
                                    ASN_Number = girASN.split(' ', 1)[0] # AS36351
                                    ASN_Number = ASN_Number[2:]
                                    ASN_Name = girASN.split(' ', 1)[1]   # Amazon.com, Inc.
                                    ASN_Name = re.sub('[ ](?=[ ])|[^-_,A-Za-z0-9. ]+', '', ASN_Name)
                                except ValueError:
                                    raise
                            else:
                                ASN_Number = 0
                                ASN_Name = "na"
                            #---------- Generate Output ---------------------------------------------
                            if gir['city'] is not None:
                                TempOutputDict['City'] = str(gir['city']).decode('utf-8', 'ignore')
                            else:
                                TempOutputDict['City'] = "na"
                                
                            if gir['region'] is not None:
                                TempOutputDict['State'] = unicode(gir['region'], "utf-8")
                            else:
                                TempOutputDict['State'] = "na"

                            if gir['country_code'] is not None:
                                TempOutputDict['Country'] = unicode(gir['country_code'], "utf-8")
                            else:
                                TempOutputDict['Country'] = "na"

                            #TempOutputDict['latitude'] = gir['latitude']
                            #TempOutputDict['longitude'] = gir['longitude']
                            TempOutputDict['Extra'] = str(gir['latitude']) + "," + str(gir['longitude'])
                            TempOutputDict['TotalBPS'] = x.net.bps
                            TempOutputDict['TotalPPS'] = x.net.pps
                            TempOutputDict['SourceASN'] = ASN_Number
                            TempOutputDict['SourceASNName'] = ASN_Name
                            TempOutputDict['AttackType'] = misuseTypes
                            OutputDict.append(TempOutputDict)
                        else:
                            if varlocaldebugging == True:
                                print "GeoIP came back empty for IP: " + CleanIP
                    #--- Clear temp variables ---
                    TempOutputDict = None
                    gir = None
                    girASN = None
            else:
                print "Ignoring CIDR: " + x.id

        if varlocaldebugging == True:
            print "DONE! Found ", SourcesFound, " Sources! \n"

#------------ Send To Info Sharing Provider ------------
        TempOutputDict_ALL['dis-data'] = OutputDict
        try:
            if varlocaldebugging == True:
                print "Sending the following to: ", varRemoteURL, "\n\n"
                print json.dumps(TempOutputDict_ALL, indent=4, sort_keys=True, ensure_ascii=False, encoding='latin1')
        except ValueError:
            print "Local debugging error: ", sys.exc_info()[0]
            raise

        try:
            req = urllib2.Request(varRemoteURL, headers=hdr)
            try:
                page = urllib2.urlopen(req, json.dumps(TempOutputDict_ALL, ensure_ascii=False, encoding='latin1'))
                content = page.read()
                print content
            except urllib2.HTTPError, e:
                print "Error Fp Read: ", e.fp.read()
                print "CODE: ", e.code()
                print "ERROR READ: ",e.read()
        except ValueError:
            print "HTTP POST had a problem", sys.exc_info()[0]
            raise

        try:
            if varlocal_log_to_file == True:
                print "logging to file... "
                try:
                    with open(varLogFile, "a") as myfile:
                        myfile.write(json.dumps(TempOutputDict_ALL, indent=4, sort_keys=True))
                        myfile.close
                except ValueError:
                    raise
        except ValueError:
            print "Logging to file had a problem", sys.exc_info()[0]
            raise

        print "All Done!"
    else:
        print "Sources came back empty for Alert: " + varArgumentReceieved
        sys.exit(0)
except ValueError:
    #print "Had a problem parsing the output", sys.exc_info()[0]
    raise
