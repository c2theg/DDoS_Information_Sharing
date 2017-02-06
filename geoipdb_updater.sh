clear
echo "Maxmind GeoIP db download script"
echo " -- Downloading files from: http://dev.maxmind.com/geoip/legacy/geolite/  --"
echo " "
echo " "
echo " "
download()
{
    maxmindURL="http://geolite.maxmind.com/download/geoip/database"
    libpath="libraries/maxmind"
    MyPath=$(pwd)
 
    local AdditionalDownloadPath=$1
    local DownloadFile=$2
    local newFile=$3

    if [ -s "$MyPath/$DownloadFile" ] 
    then
        "$MyPath/$DownloadFile" 
    fi
    
    echo "Downloading to path: $MyPath"
    #----- Remove old files ----------------------------
    if [ -s $MyPath/$libpath/$newFile ]
    then
        echo  "Removing old file - $MyPath/$libpath/$newFile"
        rm $MyPath/$libpath/$newFile
    else
        echo "File does not exist, ($MyPath/$libpath/$newFile) so download it!"
    fi       
    #-------------------------------------------------------------
    #FullDownloadPath=$maxmindURL/$AdditionalDownloadPath$DownloadFile
    echo -n "Downloading $maxmindURL/$AdditionalDownloadPath$DownloadFile"
    echo " --- "
    echo " "  
    wget "$newFile" "$maxmindURL/$AdditionalDownloadPath$DownloadFile"
    echo "Download Complete"
    #-------------------------------------------------------------
    wait
    echo "Decompressing $DownloadFile"
    gunzip $DownloadFile
    wait
    echo "Done!"
    echo "Moving file to: $MyPath/$libpath/$newFile"
    cp $newFile $MyPath/$libpath/$newFile
    wait
    echo "Removing temp file: $MyPath/$newFile"
    rm $MyPath/$newFile
    echo " "
    echo " ---------- "
    echo " "    
}
#---------------------------- Country ----------------------------------------
file="GeoIP.dat.gz"
newFile="GeoIP.dat"
#http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz

download "/GeoLiteCountry/" $file $newFile
#--------------------------------------------------------------------
file="GeoIPv6.dat.gz"
newFile="GeoIPv6.dat"
#http://geolite.maxmind.com/download/geoip/database/GeoIPv6.dat.gz

download "" $file $newFile
#---------------------------- CITY ----------------------------------------
file="GeoLiteCity.dat.gz"
newFile="GeoLiteCity.dat"
#http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz

download "" $file $newFile
#--------------------------------------------------------------------
file="GeoLiteCityv6.dat.gz"
newFile="GeoLiteCityv6.dat"
#http://geolite.maxmind.com/download/geoip/database/GeoLiteCityv6-beta/GeoLiteCityv6.dat.gz

download "GeoLiteCityv6-beta/" $file $newFile
#------------------------- ASN -------------------------------------------
file="GeoIPASNum.dat.gz"
newFile="GeoIPASNum.dat"
#http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz

download "asnum/" $file $newFile
#--------------------------------------------------------------------
file="GeoIPASNumv6.dat.gz"
newFile="GeoIPASNumv6.dat"
#http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNumv6.dat.gz

download "asnum/" $file $newFile
#--------------------------------------------------------------------

echo "Done updating all databases!"