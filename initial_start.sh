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
sudo apt-get update
wait
sudo apt-get -y upgrade
wait
apt-get -y dist-upgrade
wait
sudo apt-get install -y ntp ntpdate ssh openssh-server libicu-dev python-software-properties python python-pip python-dev screen python3-setuptools whois
wait
sudo apt-get install -y traceroute htop sysstat iptraf iftop slurm tcptrack bmon nethogs speedometer
wait
sudo apt-get install -y build-essential checkinstall
sudo apt-get install -y python2.7-dev libxml2-dev libxslt1-dev
#---- install python dependancies ----
#-- suds --
sudo apt-get install -y python-pip
wait
sudo pip install suds-jurko
sudo pip install suds
sudo pip --upgrade install
sudo easy_install https://fedorahosted.org/releases/s/u/suds/python-suds-0.4.1.tar.gz
#-- GeoIP --
wait
sudo apt-cache search geoip
sudo apt-get install -y libgeoip-dev
sudo apt-get install -y python-geoip
wait
sudo pip install GeoIP
sudo pip install python-geoip-geolite2
#----- others ---
sudo pip install requests
#----- Done -----
sudo chmod +x collector.py
sudo chmod +x getSources.py
sudo chmod +x geoipdb_updater.sh
wait
#------ Make Directory structures -----
mkdir SDKs
cd SDKs/
mkdir SDKs/6.0/
mkdir SDKs/7.0/
mkdir SDKs/7.6/
mkdir SDKs/8.0/
mkdir SDKs/8.1/
cd ..
#-----------------
mkdir libraries
cd libraries/
mkdir maxmind
cd ..
#-----------------
#sudo chmod g-wx,o-wx ~/.python-eggs
wait
#----- Cronjob to download/update Maxmind db ------
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "20 4 * */1 3 echo $MyPath/geoipdb_updater.sh" >> mycron
#install new cron file
crontab mycron
rm mycron
#----- Done -----
echo "Running GeoIP db updater"
sh ./geoipdb_updater.sh
wait
clear
echo "All done...   Starting DDoS Infomation Sharing application!"
sudo python ./collector.py