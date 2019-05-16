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


                          ___ __  _  __         ___ __  _ ____
                         |_  )  \/ |/ /   ___  |_  )  \/ |__  |
                          / / () | / _ \ |___|  / / () | | / /
                         /___\__/|_\___/       /___\__/|_|/_/



                   DDoS Source Information Sharing - Data Collector
                                    Version: 0.0.2
                                       2/5/2017
                    https://github.com/c2theg/DDoS_Infomation_Sharing
                    
------------------------------------------------------------------------------------------------
    1) Collector application
    2) GetSources application 
    3) CableLabs - Crits message information    
    4) General Info
    5) Copyright notice
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
    3) CableLabs - Crits message information

        Information about using the DDoS Info Sharing API to upload dis-data
        The website is: https://dis-demo.cablelabs.com
        
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
                
        The data is sent in real-time, as soon as the attack is over. 
------------------------------------------------------------------------------------------------        
    4) General Info
    
        The information sharing apps were both created on my spare time, outside of work hours and office. 
        No employer owned hardware equipment was used in the development of this app.
        The application was developed using python 2.7
        The server used for testing was running Ubuntu Server 14.04.5 - x86-64 Edition
        
        This product includes GeoLite2 data created by MaxMind, available from <a href="http://www.maxmind.com">http://www.maxmind.com</a>.        
        You can get new releases of the database at: https://dev.maxmind.com/geoip/legacy/geolite/
        
        This app also uses suds 0.4 https://pypi.python.org/pypi/suds for SOAP integrations.

------------------------------------------------------------------------------------------------            
    5) Copyright
        
        Copyright © 2016-2017 by Christopher MJ Gray & Daniel Phan    
        
        All rights reserved.  Proprietary and Confidential.  No part of this application may be decompiled, decrypted, deobfuscation, reproduced, distributed, or transmitted in any form or by any means, 
        Including but not limited to photocopying, recording, sniffing, d-trace, or other electronic, physical or mechanical methods, without the prior written permission of the publisher, 
        Except in the case of brief quotations embodied in critical reviews and certain other noncommercial uses permitted by copyright law. 
        For permission requests, write to the publisher, addressed “Attention: Permissions Coordinator,” at the address below.

        Christopher MJ Gray
        christophermjgray@gmail.com
