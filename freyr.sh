#!/bin/bash

## Basics
# Dates
DATE=$(date +"%Y-%m-%d")
DATETIME=$(date +"%Y-%m-%d_%H%M")

mkdir -p log

## Collect Data

echo $DATETIME "; running sense01-DHT22_v2" >> log/$DATE.log
python sense01-DHT22_v2.py

echo $DATETIME "; running sense02-DHT22_v2" >> log/$DATE.log
python sense02-DHT22_v2.py

echo $DATETIME "; running sense00-readPi_v2a" >> log/$DATE.log
python sense00-readPi_v2a.py

## Clean Data
#echo $DATETIME "; running freyr_dq_scanner_v2d.R (TST)" >> log/$DATE.log
#R CMD BATCH freyr_dq_scanner_v2d.R

# no cleaning yet

## Analyse Data
# no analysation yet

## Report Data
#no reporting yet


## Administration
echo $DATETIME "; running reconnect-wifi0" >> log/$DATE.log
bash reconnect-wifi0.bash
