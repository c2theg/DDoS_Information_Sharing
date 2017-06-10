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
Version:  0.5             \r\n
Last Updated:  6/10/2017
\r\n \r\n
Updating system first..."
sudo apt-get update 
wait
sudo apt-get upgrade -y
wait
#--------------------------------------------------------------------------------------------
echo "Downloading files..."
if [ -s "getSources.py" ] 
then
    echo "Deleting files"
    rm updater.sh
    rm collector.py
    rm getSources.py
    rm config.json.new
fi

echo "Downloading latest versions..."

sudo wget "updater.sh" "https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/updater.sh"
sudo wget "collector.py" "https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/collector.py"
sudo wget "getSources.py" "https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/getSources.py"
sudo wget "config.json.new" "https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/config.json"

wait
chmod u+x updater.sh
chmod u+x collector.py
chmod u+x getSources.py

echo "Done! \r\n \r\n"

python2.7 collector.py -c config.json
