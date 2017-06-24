#!/bin/sh
#    If you update this from Windows, using Notepad ++, do the following:
#       sudo apt-get -y install dos2unix
#       dos2unix <FILE>
#       chmod u+x <FILE>
#
clear
echo "
 _____             _         _    _          _                                   
|     |___ ___ ___| |_ ___ _| |  | |_ _ _   |_|                                  
|   --|  _| -_| .'|  _| -_| . |  | . | | |   _                                   
|_____|_| |___|__,|_| |___|___|  |___|_  |  |_|                                  
                                     |___|                                       
                                                                                 
 _____ _       _     _           _              _____    __    _____             
|     | |_ ___|_|___| |_ ___ ___| |_ ___ ___   |     |__|  |  |   __|___ ___ _ _ 
|   --|   |  _| |_ -|  _| . | . |   | -_|  _|  | | | |  |  |  |  |  |  _| .'| | |
|_____|_|_|_| |_|___|_| |___|  _|_|_|___|_|    |_|_|_|_____|  |_____|_| |__,|_  |
                            |_|                                             |___|
\r\n \r\n
Version:  0.5.4             \r\n
Last Updated:  6/24/2017
\r\n \r\n
Updating system first..."
sudo apt-get update 
wait
sudo apt-get upgrade -y
wait
#--------------------------------------------------------------------------------------------
if [ -s "getSources.py" ] 
then
    echo "Deleting old files!!!"
    rm updater.sh
    rm collector.py
    rm getSources.py
    rm func_REST.py
    rm client.html
    rm client_submissions.html
    rm config.json.new
fi

#------------------------------
echo "\n\n\n\n"
echo "Downloading latest versions to all files ... \n\n\n\n"

sudo wget -O updater.sh "https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/updater.sh"
sudo wget -O func_REST.py "https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/func_REST.py"
sudo wget -O func_common.py "https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/func_common.py"
sudo wget -O collector.py "https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/collector.py"
sudo wget -O getSources.py "https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/getSources.py"
sudo wget -O config.json.new "https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/config.json"

sudo wget -0 client.html "https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/client.html"
sudo wget -0 client_submissions.html "https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/client_submissions.html"

wait
echo "\n\n\n Done... \n\n"
#----- Update priv. -----------
chmod u+x updater.sh
chmod u+x collector.py
chmod u+x getSources.py
chmod u+x func_REST.py
#------------------------------
echo "Done! \r\n \r\n"
python2 ./collector.py -c config.json
