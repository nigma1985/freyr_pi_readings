#/bin/bash

echo "-- UPDATE --" > update.txt 
sudo apt-get update -y >> update.txt

echo "-- UPGRADE --" >> update.txt 
sudo apt-get upgrade -y >> update.txt 

echo "-- DIST UPGRADE --" >> update.txt
sudo apt-get dist-upgrade -y >> update.txt 

echo "-- AUTOCLEAN --" >> update.txt 
sudo apt-get autoclean -y >> update.txt 

cat update.txt
