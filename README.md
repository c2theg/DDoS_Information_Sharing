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
                                    Version: 0.2.32
                                       6/24/2017
                    https://github.com/c2theg/DDoS_Infomation_Sharing
                    
------------------------------------------------------------------------------------------------
    0) TL;DR:  - Gimme Gimme Gimme 
    1) Collector application
    2) GetSources application 
    3) Client Config
    4) Arbor SP config
    5) CableLabs - Crits message information    
    6) General Info
    7) Troubleshooting
    8) Copyright Notice
    9) References

------------------------------------------------------------------------------------------------
    0) TL;DR:  - Gimme Gimme Gimme
        1) Unfortunately you have to setup the config.json file first. It's not hard, just a few values need to be changed, which are documented in Section 3.
    
        2) When you're done with that, and you setup Arbor SP (Section 4) to send the syslog traffic to your server, just run this command
        
            wget https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/initial_start.sh && sudo chmod u+x ./initial_start.sh && sudo ./initial_start.sh
         
        
        
       DONE! Wasn't that easy?!?!
          
  *** FOR QUICK UPDATING (once you already had it running) ***
     
     sudo ./updater.sh
         
PLEASE RUN IT TWICE, as the updater.sh script itself gets updated with new files to download, as the application continue's to evolve.
        
     2 cronjobs are added to the server. 
          1) to start collector.py on startup, 
          2) to run updater.py every 10 days. 
              - Incase you want to know when this is ran, a line above it can be un-remmed, to send an email. (You will have to configure SMTP on your server for this to work)
         
      
        Ok now that it's all done and running, move on to read the rest. (Please) 
------------------------------------------------------------------------------------------------ 
    1) Collector application
    
        Collector.py is a syslog collector that was written to look for specific logs from Arbor SP. In the future it will be expanded to work for other vendors. 
        Its settings are stored in config.json. If you make changes to config.json, the application will need to be restarted to reflect said changes.
        
        How it works.
        
        When a log comes in, that has the special phrase collector.py is looking for (ie: ", is now done,")  the application will start a new process for the
        DDoS data collector application, getSources.py. This applications' name can be defined in the config.json file. When the collector application is done, it will close itself.         
        
        The syslog collector application should be ran at all times. The following are examples on how to start it automatically at system startup, in a crontab.
        
        crontab -e
        @reboot /usr/bin/sudo python2 /home/ubuntu/DDoS/collector.py -c /home/ubuntu/DDoS/config.json &

      
        You can launch the app by issuing the following command, in an Ubuntu Linux ssh window (i used putty)
    
        python2 ./collector.py -c /home/ubuntu/DDoS/config.json -v arbor
    
 ------------------------------------------------------------------------------------------------
    2) GetSources application

        getSources.py is an application that makes api calls out to Arbor SP. Its single threaded, so multiple copies might be running at any given time, with different command line
        Arguments sent to it.  getSources.py can also be run directly by the user, for debugging and testing. The config.json file has a few options for debugging, and logging
        Locally to view the output it is sending to the remote collection server.

        getSources.py takes in 3 parameters. 
           -c <CONFIG.JSON URL>
           -v (Vendor  - Arbor is the only one currently)
           -a (Alert ID)
        Here is an example on how to run it directly.
        
        python2 ./getSources.py -c /home/ubuntu/DDoS/config.json -v arbor -a 123456
    
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
                asn  (Just the number. no need for the as prefix. e.g.: "1234")
                
        I will try not to add too much to the config over time, but this is beta, so the config might change overtime.         
        
        The following is the default config:   
        
            {
                "identity": {
                    "company_type": "isp",
                    "name":         "<COMPANY NAME>",
                    "asn":          1234,
                    "domain":       "<Company URL>.com",
                    "callback_url": ""
                },
                "local": {
                    "default_vendor":   "arbor",
                    "output_debug":     true,
                    "wait_before_pull": 2,
                    "timezone":         "America/New_York",
                    "proxy":            false,
                    "proxy_username":   "",
                    "proxy_passwd":     "",
                    "proxy_url":        "",
                    "proxy_port":       "",
                    "auto_updates":     false,
                    "updates_url":      "https://github.com/c2theg/DDoS_Infomation_Sharing/archive/master.zip",
                    "update_checkEvery": 5
                },
                "email": {
                    "enabled":  false,
                    "server":   "mailrelay.server.com",
                    "port":     465,
                    "auth":     false,
                    "username": "",
                    "passwd":   "",
                    "from":     "ddos_info_sharing_1@company.com"
                },
                "email_recipients": [
                    { "to": "admin@carrier.com", "name": "John Smith", "cc":"", "bcc": "", "send_info": false, "send_errors": true },
                    { "to": "admin@carrier.com", "name": "Jane Doe", "cc":"", "bcc": "", "send_info": false, "send_errors": false }
                ],
                "remote": [ 
                    { "url": "https://dis-demo2.cablelabs.com/api/v1/data_ingester_resource/?username=<USER_NAME>&api_key=<API_KEY>", "label": "Dev", "format": "json", "send_infosharing": true, "send_details": false, "timeout": 120, "extra": "", "proto": "tcp" }
                ],
                "geo": {
                    "enabled_forSending":      false,
                    "enabled_forReceiving":    true,
                    "files_path":              "libraries/maxmind/",
                    "update_url":              "http://dev.maxmind.com/geoip/legacy/geolite/"
                },
                "arbor": {
                    "version":             7.6,   
                    "syslog_trigger_on":   ", is now done,",
                    "syslog_port":         1514,
                    "syslog_proto":        "udp",    
                    "url":                 "10.1.1.1",
                    "port":                443,
                    "key":                 "<ARBOR_KEY>",
                    "user":                "arbor",
                    "zone_secret":         "<PASSWORD>",
                    "wsdl":                "PeakflowSP.wsdl",
                    "source_collector":    "getSources.py",
                    "log_to_file":         false,
                    "log_file":            "/var/log/ddos_infosharing_arbor_log.txt",
                    "log_file_errors":     "/var/log/ddos_infosharing_arbor_error_log.txt" 
                },
                "a10": {
                    "version":             4.2,
                    "syslog_trigger_on":   " done ",
                    "syslog_port":         1515,
                    "syslog_proto":        "udp",    
                    "url":                 "10.1.1.1",
                    "port":                443,
                    "user":                "a10",
                    "password":            "<PASSWORD>",
                    "source_collector":    "getSources_a10.py",
                    "log_to_file":         false,
                    "log_file":            "/var/log/ddos_infosharing_a10_log.txt",
                    "log_file_errors":     "/var/log/ddos_infosharing_a10_error_log.txt" 
                },
                "radware": {
                    "version":             3.8,
                    "syslog_trigger_on":   " done ",
                    "syslog_port":         1516,
                    "syslog_proto":        "udp",
                    "url":                 "10.1.1.1",
                    "port":                443,
                    "user":                "radware",
                    "password":            "<PASSWORD>",
                    "source_collector":    "getSources_radware.py",
                    "log_to_file":         false,
                    "log_file":            "/var/log/ddos_infosharing_radware_log.txt",
                    "log_file_errors":     "/var/log/ddos_infosharing_radware_error_log.txt" 
                },
                "f5": {
                    "version":             12.2,
                    "syslog_trigger_on":   " Attack Stopped ",
                    "syslog_port":         1517,
                    "syslog_proto":        "udp",    
                    "url":                 "10.1.1.1",
                    "port":                443,
                    "user":                "admin",
                    "password":            "<PASSWORD>",
                    "source_collector":    "getSources_f5.py",
                    "log_to_file":         false,
                    "log_file":            "/var/log/ddos_infosharing_f5_log.txt",
                    "log_file_errors":     "/var/log/ddos_infosharing_f5_error_log.txt" 
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
        The current website is: https://dis-demo2.cablelabs.com
        
        Login and get your API key, on this page: https://dis-demo.cablelabs.com/profile/#api_button
        
        API URI:

        https://dis-demo2.cablelabs.com/api/v1/data_ingester_resource/?username=<USER_NAME>&api_key=<API_KEY>

        Replace <USERNAME> and <API_KEY> with the information sent in the email

        Payload Headers:
        "Content-Type": application/json

        Payload Body:
        
        {
            "ProviderName": "SomeISP",
            "dis-data": [
                {
                    "IPaddress": "192.168.1.1",
                    "attackStartTime": "2017-11-27T03:17:45z",
                    "attackStopTime": "2017-11-27T03:25:36z",
                    "attackTypes": [
                        "IP Fragmentation"
                    ],
                    "peakBPS": 179915,
                    "peakPPS": 14
                },
                {
                    "IPaddress": "10.1.1.1",
                    "attackStartTime": "2017-11-27T03:17:45z",
                    "attackStopTime": "2017-11-27T03:25:36z",
                    "attackTypes": [
                        "IP Fragmentation"
                    ],
                    "peakBPS": 1269915,
                    "peakPPS": 163
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
    7) Troubleshooting
    
      Check if the port is open: 
          netstat -tulnp | grep 1514
        
      Check to see if your getting data:  
          tcpdump udp -i any -nn -t -v dst port 1514
          
      Show Processes:  (nicer version of top)
          htop 

------------------------------------------------------------------------------------------------
    8) Copyright
        
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
    9) References
    
        Cable Labs 
            https://cablelabs.github.io/ddos-info-sharing/
            https://github.com/cablelabs/ddos-info-sharing
            https://dis-demo2.cablelabs.com/ips/list/  
