#!/bin/bash

## Basics
# Dates
DATE=$(date -u +"%Y-%m-%d")
DATETIME=$(date -u +"%Y-%m-%d_%H%M")
IAM="byangoma"
#OUT_FILE="out\/FREYR\_$DATETIME\_$IAM.csv"

python freyr_pi_readings/tst.py out/FREYR_$DATETIME\_$IAM.csv

# DATA_HEAD="value | pin | utc_1 | utc_2 | offsetutc | duration_sec | outdoors_name | loc_lat | loc_long | loc_description | provider_type | source_name | source_description | periphery_type | periphery_name | periphery_description | periphery_device_description | measure_name | measure_sign | measure_type_full | measure_type_abbr | measure_absolute_min | measure_absolute_max | measure_target_type | measure_target_name | measure_target_description | data_quality"
#
# mkdir -p log
# mkdir -p out
# mkdir -p in
# mkdir -p archive

## Collect Data
#echo $DATA_HEAD >> out/FREYR_$DATETIME\_$IAM.csv

#python freyr_pi_readings/readPi.py out/FREYR_$DATETIME\_$IAM.csv

#python readEnviro_v2b.py out/FREYR_$DATETIME\_$IAM.csv

## Clean Data
# no cleaning yet

## Analyse Data
# no analysation yet

## Report Data
#no reporting yet


# NTW=$(python maintenance.py out/FREYR_$DATETIME\_$IAM.csv | tail -n 1)
#
# if [ "$NTW" = "ok" ]; then
#   echo "OK!"
# elif [ "$NTW" = "err" ]; then
#   echo "ERROR!"
# elif [ "$NTW" = "reboot" ]; then
#   echo "last resort ... "
#   sudo reboot
# else
#   echo "RECONNECT WIFI"
#   sudo /sbin/ifdown '$NTW'
#   sleep 5
#   sudo /sbin/ifup --force '$NTW'
#   # sleep 20
# fi
