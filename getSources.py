#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (c) 2016-2017 Christopher Gray & Daniel Phan - Comcast Cable Communications LLC.
# All rights reserved.
# https://github.com/c2theg/DDoS_Infomation_Sharing

#--- Force Python2 as Suds doesn't support Python3 fully as of 11/10/2016
#This product includes GeoLite2 data created by MaxMind, available from http://www.maxmind.com
#Inital: 12/23/16  Updated: 2/5/17
#from socket import *
import socket
from io import StringIO
from datetime import datetime
import errno, sys, json, os, time, logging, argparse, base64, ssl, re, string, inspect
import urllib2
#from pprint import pprint
#------- Suds ------- 
# https://pypi.python.org/pypi/suds
# https://pypi.python.org/pypi/suds-jurko/0.6
# https://jortel.fedorapeople.org/suds/doc/suds.options.Options-class.html
# https://bitbucket.org/jurko/suds
import suds
import suds.client
#------ MaxMind Legacy and GeoIP2 API's ------  
try:
    import GeoIP # https://github.com/maxmind/geoip-api-python
    import geoip2.database  # GeoIP2 - https://github.com/maxmind/GeoIP2-python 
except OSError:
    pass
#---- Custom Libraries ----
# Add current dir to search path.
#sys.path.insert(0, "libraries")
#pprint(sys.path)
#import func_REST
from func_REST import *
#from libraries.func_REST import *
#import func_REST
cls_http = HTTP_Classes()  # instantiate HTTP REST class
#------ Variables ------
reload(sys)
sys.setdefaultencoding('utf8')
PythonVer = sys.version_info
appCurrentPath = os.getcwd()
appCurrentPath.replace("\/",'\\/')
appTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
appVersion = '0.2.23'
SourcesFound = 0
OutputDict = []
OutputJSON = ""
SendData = []
app_hostname = socket.getfqdn()
print "Hostname: " + app_hostname
#---- Import Config ----- 
try:
    ConfigFilePath = appCurrentPath + '/config.json'
    #print "Loading Config file: ", ConfigFilePath
    with open(ConfigFilePath) as data_file:
        configData = json.load(data_file)
        #----------------------------------------
    #print "Config Data: ", configData
    varUpdate_auto = configData['local']['auto_updates']
    varUpdate_url = configData['local']['updates_url']
    varUpdate_checkEvery = configData['local']['update_checkEvery']
    #-----------------------------------------------------------------
    varArborURL = 'https://' + configData['arbor']['url']
    varArborPort = configData['arbor']['port']
    varArborKey = configData['arbor']['key']
    varArborVersion = configData['arbor']['version']
    varArborUser = configData['arbor']['user']
    varArborPasswd = configData['arbor']['zone_secret']
    varArborWSDL = 'SDKs/' + str(varArborVersion) + '/' + configData['arbor']['wsdl']
    WSDLfile =  appCurrentPath + "/" + varArborWSDL
    if os.path.isfile(WSDLfile):
        print "WSDL file loaded!"
    else:
        print "WSDL file (", WSDLfile, ") DOES NOT exist! Please download the Arbor SDK and put the WSDL in the correct location under SDKs/<Version>/  and make sure its set correctly in config.json"
        sys.exit(0)
    #-----------------------------------------------------------------
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
    varRemoteURL = configData['remote']


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

if sys.version_info < (2, 7, 9):
    print 'Insecure TLS/SSL detected: upgrade to Python 2.7.9+ to prevent TLS errors'
    
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    print "Legacy Python " + str(PythonVer) + " doesn't verify HTTPS TLS 1.0+ certificates by default."
    #ssl._create_default_https_context = ssl._create_unverified_context  #SSL fix for python 2.7.6+
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    #ssl._create_default_https_context = _create_unverified_https_context
    ssl._create_default_https_context = ssl._create_unverified_context  #SSL fix for python 2.7.6+

page = ''
#-------------- Get the GeoIP Database file ------------------------------------------------------------------------------
print 'This product includes GeoLite2 data created by MaxMind, available from <a href="http://www.maxmind.com">http://www.maxmind.com</a>.'
if varlocaldebugging == True:
    print "Loading the following Maxmind GeoIP database from path: " + varGeoIPDir + ", GeoLite2-City.mmdb, GeoIPASNum.dat, GeoIPASNumv6.dat \n\n"    
try:
    geoIP2_City     = geoip2.database.Reader(varGeoIPDir + 'GeoLite2-City.mmdb')
    geoipASN_v4     = GeoIP.open(varGeoIPDir + "GeoIPASNum.dat",    GeoIP.GEOIP_MEMORY_CACHE) #--- Needed as GeoIP2 doesn't offer ASN for free ---
    geoipASN_v6     = GeoIP.open(varGeoIPDir + "GeoIPASNumv6.dat",  GeoIP.GEOIP_MEMORY_CACHE)
except OSError:
    print "Could not load GeoIP file(s)! Please run \n"
    sys.exit(0)
#-------------------------------------------------------------------------------------------------------------------------    
print "Waiting " + str(varlocal_wait_before_pull) + " seconds before pulling data from Arbor."
time.sleep(varlocal_wait_before_pull)
#-------------------------------------------------------------------------------------------------------------------------
misuseTypes = ''
try:
    alertDetailsResponseRAW = cls_http.HTTP_GET_rjson( str(varArborURL + "/arborws/alerts?api_key=" + varArborKey + "&filter=" + varArgumentReceieved) )

    for i in alertDetailsResponseRAW:
        misuseTypes += str(i['misuseTypes'])
    misuseTypes = misuseTypes[1:]  # [u'TCP SYN']
    misuseTypes = misuseTypes[:-1]  # [u'TCP SYN']
    misuseTypes = misuseTypes.replace("u'", "")
    misuseTypes = misuseTypes.replace("'", "")
    print "Misuse Type(s): "  + misuseTypes
    
except OSError:
    print "Could not fetch Alert Details. " +  sys.exc_info()[0]
#--------------------------------------------------------------------------------------------------------------------------
'''
try:
    print "getting mitigation data... "
    mitDetailsResponseRAW = cls_http.HTTP_GET_rjson( str(varArborURL + "/arborws/mitigations/status?api_key=" + varArborKey + "&filter=" + varArgumentReceieved), 0)
    print "mitDetailsResponseRAW: " 
    print json.dumps(mitDetailsResponseRAW, indent=4, sort_keys=True, ensure_ascii=False, encoding='latin1')
except OSError:
    print "Could not fetch Alert Details. " +  sys.exc_info()[0]
'''
#--------------------------------------------------------------------------------------------------------------------------
if varlocaldebugging == True:
    print "Connecting to:",varArborURL," User: ",varArborUser, " WSDL: " + WSDLfile
try:
    t = suds.transport.https.HttpAuthenticated(username=varArborUser, password=varArborPasswd)
    t.handler = urllib2.HTTPDigestAuthHandler(t.pm)
    t.urlopener = urllib2.build_opener(t.handler)
    client = suds.client.Client(url='file:///' + WSDLfile, location=varArborURL + '/soap/sp', transport=t)
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
            if ('/32' in x.id or '/128' in x.id):
                if x.net.bps != 0:
                    if x.net.pps != 0:
                        #print "IP Address: ", x.id, "BPS: ", x.net.bps, "PPS: ", x.net.pps
                        SourcesFound += 1
                        TempOutputDict = {}
                        CleanIP = x.id.split("/")[0]                    
                        TempOutputDict['IPaddress'] = CleanIP
                        #---- do GeoIP Lookup ----------
                        gir = geoIP2_City.city(CleanIP)
                        if gir is not None:
                            #------------ ASN ---------
                            if ':' in x.id:  # this is a IPv6 Address
                                girASN = geoipASN_v6.org_by_addr(CleanIP)
                            else:
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
                            if gir.city.name is not None:
                                TempOutputDict['City'] = str(gir.city.name).decode('utf-8', 'ignore')
                            else:
                                TempOutputDict['City'] = "na"
                                
                            if gir.subdivisions.most_specific.iso_code is not None:
                                TempOutputDict['State'] = str(gir.subdivisions.most_specific.iso_code).decode("utf-8", 'ignore')
                            else:
                                TempOutputDict['State'] = "na"

                            if gir.country.iso_code is not None:
                                TempOutputDict['Country'] = str(gir.country.iso_code).decode("utf-8", 'ignore') # 'US'
                            else:
                                TempOutputDict['Country'] = "na"

                            #TempOutputDict['latitude'] = gir.location.latitude
                            #TempOutputDict['longitude'] = gir.location.longitude
                            TempOutputDict['Extra'] = str(gir.location.latitude) + "," + str(gir.location.longitude)
                            TempOutputDict['TotalBPS'] = x.net.bps
                            TempOutputDict['TotalPPS'] = x.net.pps
                            TempOutputDict['SourceASN'] = ASN_Number
                            TempOutputDict['SourceASNName'] = ASN_Name 
                            TempOutputDict['AttackType'] = misuseTypes
                            #print "Work on: " + TempOutputDict
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

        geoIP2_City.close()

        if varlocaldebugging == True:
            print "\n\n Finished generating JSON payload, which containes ", SourcesFound, " DDoS sources! \n\n"

        #------------ Send To Info Sharing Provider(s) ------------
        if varRemoteURL is not None:
            TempOutputDict_ALL['dis-data'] = OutputDict          
            try:
                if varlocaldebugging == True:
                    print "Sending the following: \n"
                    print json.dumps(TempOutputDict_ALL, indent=4, sort_keys=True, ensure_ascii=False, encoding='latin1')
            except ValueError:
                print "Local debugging error: ", sys.exc_info()[0]
                raise

            for i in configData['remote']:
                print "\n"
                ProviderResponse = cls_http.HTTP_POST_SendJson(i['url'], TempOutputDict_ALL)
                if varlocaldebugging == True:
                    print ProviderResponse
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
