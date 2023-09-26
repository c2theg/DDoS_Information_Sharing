clear
echo "Maxmind GeoIP db download script"
echo " -- Downloading files from: http://dev.maxmind.com/geoip/legacy/geolite/  --"
echo " "
echo " "
echo " "
download()
{
    maxmindURL="https://geolite.maxmind.com/download/geoip/database"
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

#---------------------------- GeoIP2 Lite City ----------------------------------------
file="GeoLite2-City.mmdb.gz"
newFile="GeoLite2-City.mmdb"
#http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz

download "" $file $newFile
#------------------------- ASN -------------------------------------------
file="GeoIPASNum.dat.gz"
newFile="GeoIPASNum.dat"
#https://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz

download "asnum/" $file $newFile
#--------------------------------------------------------------------
file="GeoIPASNumv6.dat.gz"
newFile="GeoIPASNumv6.dat"
#https://download.maxmind.com/download/geoip/database/asnum/GeoIPASNumv6.dat.gz

download "asnum/" $file $newFile
#--------------------------------------------------------------------

echo "Done updating all databases!"
