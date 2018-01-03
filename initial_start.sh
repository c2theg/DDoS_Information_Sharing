#!/bin/sh
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
\r\n \r\n"
MyPath=$(pwd)
echo "Working out of directory: $MyPath \r\n \r\n"
echo "---------------------------------------------------------------------------------------------------------------"
# -- add newer python 2.7.x repo --
sudo -E add-apt-repository -y ppa:fkrull/deadsnakes-python2.7
wait
sudo -E apt-get update
wait
sudo -E apt-get -y upgrade
wait
sudo apt-get -y autoremove
wait
#-- Upgrade to latest Kernal --
sudo -E apt-get -y dist-upgrade
wait
sudo -E apt-get install -y ntp ntpdate ssh openssh-server openssl libssl-dev whois traceroute htop
wait
sudo -E apt-get install -y python-software-properties python python-pip python-dev python2.7
wait
#---- install python dependancies ----
#-- suds --
#sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv
#sudo pip install suds
#sudo easy_install https://fedorahosted.org/releases/s/u/suds/python-suds-0.4.1.tar.gz

# More Info: https://pypi.python.org/pypi/suds-jurko/0.6
sudo easy_install https://pypi.python.org/packages/bd/6f/54fbf0999a606680d27c69b1ad12dfff62768ecb9fe48524cebda6eb4423/suds-jurko-0.6.tar.bz2
#sudo pip install suds-jurko
wait
sudo pip --upgrade install
wait
#----- others ---
sudo pip install requests
sudo pip install lxml
sudo pip install cssselect
wait
sudo pip install --upgrade requests
#----- Done -----
sudo chmod -R u+x .
# sudo chmod -R 755 . && sudo chown -R ubuntu:ubuntu .
wait
#------ Make Directory structures -----
SDKpath="$(pwd)/SDKs"
mkdir $SDKpath
cd $SDKpath/
mkdir 7.6/
cd 7.6/
wget https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/SDKs/7.6/PeakflowSP.wsdl
wait
cd ..
wait
cd ..
#-----------------
#mkdir libraries
#cd libraries/
#mkdir maxmind
#cd ..
#----- Cronjob to update scripts ------
line="@reboot /usr/bin/sudo python2 $MyPath/collector.py -c $MyPath/config.json &"
(sudo crontab -u root -l; echo "$line" ) | sudo crontab -u root -

echo "Run updater every 10 days, and send output to the following email address. Just remove the # in the front \r\n"
line="#MAILTO='<your email here>'"
(sudo crontab -u root -l; echo "$line" ) | sudo crontab -u root -

line="1 4 */10 * * updater.sh"
(sudo crontab -u root -l; echo "$line" ) | sudo crontab -u root -
#----------------
wget https://raw.githubusercontent.com/c2theg/DDoS_Information_Sharing/master/updater.sh
wait
sudo chmod u+x updater.sh
wait
echo "Running updater to download latest build... \r\n"
wait
sudo ./updater.sh
echo "\r\n \r\n"

echo "All done...  To start DDoS Infomation Sharing application, enter the following: "
echo "python2 ./collector.py -c $MyPath/config.json -v arbor"
