#/bin/bash

echo "-- UPDATE --" > update.txt
sudo apt-get update -y >> update.txt

echo "-- UPGRADE --" >> upgrade.txt
sudo apt-get upgrade -y >> upgrade.txt

echo "-- DIST UPGRADE --" >> dist_upgrade.txt
sudo apt-get dist-upgrade -y >> dist_upgrade.txt

echo "-- AUTOCLEAN --" >> autoclean.txt
sudo apt-get autoclean -y >> autoclean.txt

# cat update.txt
