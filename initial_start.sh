#!/bin/sh
clear
echo "
    ____  ____       _____    ____      ____                           __  _                _____ __               _            
   / __ \/ __ \____ / ___/   /  _/___  / __/___  _________ ___  ____ _/ /_(_)___  ____     / ___// /_  ____ ______(_)___  ____ _
  / / / / / / / __ \\__ \    / // __ \/ /_/ __ \/ ___/ __ `__ \/ __ `/ __/ / __ \/ __ \    \__ \/ __ \/ __ `/ ___/ / __ \/ __ `/
 / /_/ / /_/ / /_/ /__/ /  _/ // / / / __/ /_/ / /  / / / / / / /_/ / /_/ / /_/ / / / /   ___/ / / / / /_/ / /  / / / / / /_/ / 
/_____/_____/\____/____/  /___/_/ /_/_/  \____/__  /_/ /__ /_/\__,_/\__/_/\____/_/ /_/   /____/_/ /_/\__,_/_/  /_/_/ /_/\__, /  
   ________  / /___  ______     _______________(_)___  / /_                                                            /____/   
  / ___/ _ \/ __/ / / / __ \   / ___/ ___/ ___/ / __ \/ __/                                                                     
 (__  )  __/ /_/ /_/ / /_/ /  (__  ) /__/ /  / / /_/ / /_                                                                       
/____/\___/\__/\__,_/ .___/  /____/\___/_/  /_/ .___/\__/                                                                       
                   /_/                       /_/                                                                                
"
echo " "
echo " "
echo " "
MyPath=$(pwd)
echo $MyPath
echo " "
echo " "
echo "---------------------------------------------------------------------------------------------------------------"
# -- add newer python 2.7.x repo --
sudo add-apt-repository -y ppa:fkrull/deadsnakes-python2.7
wait
sudo apt-get update
wait
sudo apt-get -y upgrade
wait
#-- Upgrade to latest Kernal --
sudo apt-get -y dist-upgrade
wait
sudo apt-get install -y ntp ntpdate ssh openssh-server openssl libssl-dev whois traceroute htop
wait
sudo apt-get install -y python-software-properties python python-pip python-dev python2.7
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
#-- GeoIP --
# https://pypi.python.org/pypi/geoip2
sudo apt-cache search geoip
sudo apt-get install -y libgeoip-dev
sudo apt-get install -y python-geoip
wait
sudo pip install geoip2
sudo pip install GeoIP
sudo pip install python-geoip-geolite2
wait
#----- others ---
sudo pip install requests
sudo pip install --upgrade requests
sudo easy_install hashlib
sudo pip install certifi
sudo pip install urllib3[secure]
sudo pip install 'requests[security]'
#----- Done -----
echo $MyPath
sudo chmod -R +x .
# sudo chmod -R 755 . && sudo chown -R ubuntu:ubuntu .
wait
#------ Make Directory structures -----
#SDKpath="$(pwd)/SDKs"
#mkdir $SDKpath
#cd $SDKpath/
#mkdir 7.6/
#cd ..
#-----------------
#mkdir libraries
#cd libraries/
#mkdir maxmind
#cd ..
#-----------------
#sudo chmod g-wx,o-wx ~/.python-eggs
#wait
#----- Cronjob to download/update Maxmind db ------
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "20 4 * */1 3 echo $MyPath/geoipdb_updater.sh" >> mycron
#echo "20 4 * */1 3 echo $MyPath/updater.sh" >> mycron
#install new cron file
crontab mycron
rm mycron
#----- Done -----
echo "Running GeoIP db updater"
sudo sh ./geoipdb_updater.sh
wait
clear
echo "All done...   Starting DDoS Infomation Sharing application!"
sudo python ./collector.py