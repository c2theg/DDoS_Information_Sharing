# DDoS_Infomation_Sharing
Carrier Grade DDoS Information Sharing

This was built to interface with Arbor SP 7.6, but will be updated over time to include newer versions as well as other vendors. 
#
#

                                                                                     
     _____ _       _     _           _              _____    __    _____             
    |     | |_ ___|_|___| |_ ___ ___| |_ ___ ___   |     |__|  |  |   __|___ ___ _ _ 
    |   --|   |  _| |_ -|  _| . | . |   | -_|  _|  | | | |  |  |  |  |  |  _| .'| | |
    |_____|_|_|_| |_|___|_| |___|  _|_|_|___|_|    |_|_|_|_____|  |_____|_| |__,|_  |
                                |_|                                             |___|
                                          ___   
                                         ( _ )  
                                         / _ \/\
                                        | (_>  <
                                         \___/\/
                                                
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



                   DDoS Source Information Sharing - Data Collector
                                    Version: 0.2.27
                                       6/9/2017
                    https://github.com/c2theg/DDoS_Infomation_Sharing
                    
------------------------------------------------------------------------------------------------
    0) TL;DR:  - Gimme Gimme Gimme 
    1) Collector application
    2) GetSources application 
    3) Client Config
    4) Arbor SP config
    5) CableLabs - Crits message information    
    6) General Info
    7) Copyright Notice
    8) References

------------------------------------------------------------------------------------------------
    0) TL;DR:  - Gimme Gimme Gimme
        1) Unfortunately you have to setup the config.json file first. It's not hard, just a few values need to be changed, which are documented in Section 3.
    
        2) When you're done with that, and you setup Arbor SP (Section 4) to send the syslog traffic to your server, just run this command
        
            sudo chmod u+x ./initial_start.sh && ./initial_start.sh
    
        DONE! Wasn't that easy?!?!
        Ok now that it's all done and running, move on to read the rest. (Please) 
------------------------------------------------------------------------------------------------ 
    1) Collector application
    
        Collector.py is a syslog collector that was written to look for specific logs from Arbor SP. In the future it will be expanded to work for other vendors. 
        Its settings are stored in config.json. If you make changes to config.json, the application will need to be restarted to reflect said changes.
        
        How it works.
        
        When a log comes in, that has the special phrase collector.py is looking for (ie: ", is now done,")  the application will start a new process for the
        DDoS data collector application, getSources.py. This applications' name can be defined in the config.json file. When the collector application is done, it will close itself.         
        
        The syslog collector application should be ran at all times. The following are examples on how to start it automatically at system startup, in a crontab.
        
        
        @reboot python /home/ubuntu/collector.py > /dev/null &
    
        You can launch the app by issuing the following command, in an Ubuntu Linux ssh window (i used putty)
    
        python ./collector.py
    
 ------------------------------------------------------------------------------------------------
    2) GetSources application

        getSources.py is an application that makes api calls out to Arbor SP. Its single threaded, so multiple copies might be running at any given time, with different command line
        Arguments sent to it.  getSources.py can also be run directly by the user, for debugging and testing. The config.json file has a few options for debugging, and logging
        Locally to view the output it is sending to the remote collection server.

        getSources.py takes in 1 parameter. Which is the arbor alert id.
        Here is an example on how to run it directly.
        
        python ./getSources.py 123456
    
 ------------------------------------------------------------------------------------------------
    3) Client Config

        To get the application running there is a config file that will need to be configured first before it will work. 
        The file is config.json and is in JSON format. 
        
        Not everything needs to be changed. But a few things i would like to highlight are as follows:
            syslog_port
            Arbor ->
                url (ip address for arbor. DNS might work, but IP was tested)
                key (API key)
                version (Used to select which directory has the peakflow.wsdl file in it)
                user (admin usually)
                zone_secret (the zone secret password)
                
            identity ->
                name (your company name. IMPORTANT, needs to be the same as in the CRITS database)
                asn  (Just the number. no need for the as prefix. e.g.: "AS1234")
                
        I will try not to add too much to the config over time, but this is beta, so the config might change overtime.         
        
        The following is the default config:
        
        {
            "local": {
                "syslog_port":  	 1514,
                "syslog_proto": 	 "udp",
                "output_debug": 	 false,
                "log_to_file":  	 false,
                "log_file":     	 "/var/log/ddos_infosharing_log.txt",
                "wait_before_pull":  2,
                "timezone":     	 "America/New_York",
                "syslog_trigger_on": ", is now done,",
                "source_collector":  "getSources.py",
                "proxy":             false,
                "proxy_username":    "",
                "proxy_passwd":      "",
                "proxy_url":         "",
                "proxy_port":        "",
                "auto_updates":		 false,
                "updates_url":		 "https://github.com/c2theg/DDoS_Infomation_Sharing/archive/master.zip",
                "update_checkEvery": "5d"
            },
            "email": {
                "server":   "mailrelay.server.com",
                "port":     465,
                "auth":     false,
                "username": "",
                "passwd":   "",
                "from":     "",
                "to":       "",
                "cc":       "",
                "bcc":      ""
            },
            "remote": [ 
                {"url": "https://dis-demo.cablelabs.com/api/v1/data_ingester_resource/?username=<USER_NAME>&api_key=<API_KEY>", "label": "Dev", "format": "json", "send_infoshare": true, "send_alert": false, "send_mit": false, "extra": "" }
            ],
            "geo": {
                "files_path": 	"libraries/maxmind/",
                "update_url": 	"http://dev.maxmind.com/geoip/legacy/geolite/"
            },
            "arbor": {
                "url":      	"192.168.1.2",
                "port":     	443,
                "key":      	"<ARBOR_KEY>",
                "version":  	7.6,
                "user":     	"arbor",
                "zone_secret":  "<PASSWORD>",
                "wsdl":     	"PeakflowSP.wsdl"
            },
            "identity": {
                "company_type": "isp",
                "name":         "<COMPANY NAME>",
                "asn":          1234,
                "domain":       "<Company URL>.com",
                "callback_url": ""
            }
        }
 
------------------------------------------------------------------------------------------------        
    4) Arbor SP config
        
        For this to work you need to configure Arbor SP to forward SYSLOGs to the server running this script on the port and protocol defined in the config.json file.
        
        You accomplish this with the following steps:
            1) Login to arbor with an admin account
            2) Go to: Administration -> Notification -> Groups
            3) Click the "Add Notification Group" button at the mid-top right hand side of the page. 
            4) Fill out your server info. Attached file "Notification_Group1.PNG" is an example of this
            
            5) Then browse to: Administration -> Notification -> Rules
            6) Click the "Add Rule" button at the mid-top right hand side of the page. 
            7) Fill out settings in the image "Notification_Rule1.PNG"
                e.g.:  CIDR: 0.0.0.0/0
                     Importance:  medium   (High is included in medium, so no need for a separate rule)
                     Notification Group (Select the one you made in step 4)
        
            8) Commit changes at the top.  Arbor will start forwarding traffic once completed.         

------------------------------------------------------------------------------------------------        
    5) CableLabs - CRITS message information

        Information about using the DDoS Info Sharing API to upload dis-data
        The current website is: https://dis-demo.cablelabs.com
        
        Login and get your API key, on this page: https://dis-demo.cablelabs.com/profile/#api_button
        
        API URI:

        https://dis-demo.cablelabs.com/api/v1/data_ingester_resource/?username=%USERNAME%&api_key=%API_KEY%

        Replace %USERNAME% and %API_KEY% with the information sent in the email

        Payload Headers:
        "Content-Type": application/json

        Payload Body:
        {
            "ProviderASN": 1234,
            "ProviderName": "SomeISP",
            "company_type": "isp",
            "dis-data": [
                {
                    "AttackType": "IP Fragmentation",
                    "City": "Columbus",
                    "Country": "NJ",
                    "Extra": "00.0000,00.0000",
                    "IPaddress": "192.168.1.1",
                    "SourceASN": "54321",
                    "SourceASNName": "Big Company LLC",
                    "State": "CA",
                    "TotalBPS": 322439,
                    "TotalPPS": 27
                },
                {
                    "AttackType": "IP Fragmentation",
                    "City": "Moscow",
                    "Country": "RU",
                    "Extra": "42.6666984558,21.1667003632",
                    "IPaddress": "10.1.1.1",
                    "SourceASN": "39237",
                    "SourceASNName": "I.T.S",
                    "State": "00",
                    "TotalBPS": 163841,
                    "TotalPPS": 13
                }
            ]
        }


        Note that, besides "IPaddress" and "ProviderName", all other fields are optional for now.
                
        The data is sent in real-time, as soon as the attack is over. It has to be AFTER for Arbor to have the source ip data.
        
        I deeply care about security, so I do not send any data that is specific about the company hosting the data.
        This includes but is not limited to:
            Usernames, Passwords, API keys, Attack data not useful in sharing, etc. 
        
        That being said, future versions will allow you to forward more detailed data that would have attack and mitigation data, but never auth credentials, to other 3rd party sources.
        Sending of Alert and Mitigation data is OFF by default, and set on a per destination basis’s. 
        These options are OFF BY DEFAULT, and that will never change!
------------------------------------------------------------------------------------------------        
    6) General Info
    
        The application was developed using python 2.7.x (2.7.6 then 2.7.12)
        The server used for testing was running Ubuntu Server 14.04.5 - x86-64 Edition
        
        This product includes GeoLite2 data created by MaxMind, available from <a href="http://www.maxmind.com">http://www.maxmind.com</a>.        
        You can get new releases of the database at: https://dev.maxmind.com/geoip/legacy/geolite/
        
        This app also uses suds 0.4 - 0.6 https://pypi.python.org/pypi/suds for SOAP integrations.

------------------------------------------------------------------------------------------------            
    7) Copyright
        
        Copyright © 2016-2017 by Christopher MJ Gray & Daniel Phan    
        
        All rights reserved.  Proprietary and Confidential.  No part of this application may be decompiled, decrypted, de-obfuscation, reproduced, distributed, or transmitted in any form or by any means, 
        Including but not limited to photocopying, recording, sniffing, d-trace, or other electronic, physical or mechanical methods, without the prior written permission of the publisher, 
        Except in the case of brief quotations embodied in critical reviews and certain other noncommercial uses permitted by copyright law. 
        For permission requests, write to the publisher, addressed “Attention: Permissions Coordinator,” at the address below.

        Christopher MJ Gray
        christopher_gray3@cable.comcast.com
        christophermjgray@gmail.com
        
        Many other Companies/Employees have helped to make this possible. 
        I will update this documentation with those who would like to be named, contact information. 
        
------------------------------------------------------------------------------------------------
    8) References
    
        Cable Labs 
            https://cablelabs.github.io/ddos-info-sharing/
            https://dis-demo.cablelabs.com/ips/list/        
