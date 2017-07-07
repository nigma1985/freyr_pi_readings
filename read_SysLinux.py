#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import os 
from subprocess import PIPE, Popen
import psutil
import sys
#import Adafruit_DHT
#import datetime
from datetime import datetime
from datetime import timedelta 
import time
import sqlite3 as lite


#################################################
#################################################

## Source & 
source_name = 'FreyrTST 1'
source_description = 'Test RPi3 - Freyr - Longterm Test'

## location
loc_lat = 53.304130
loc_long = 9.706472
loc_description = 'test indoor'

## Periphery
periphery_name = 'Raspberry Pi 3'
periphery_type = 'System'
periphery_description = 'Hardware'
periphery_device_description = 'tst'

## measure target
#measure_target_type = '' ## general type
CPU_measure_target_type = 'CPU'
RAM_measure_target_type = 'RAM'
Disk_measure_target_type = 'Disk' 
measure_target_name = 'System' ## 'yes' 'none' 'other'
measure_target_description = 'Monitoring Hardware' 

## Other Qualities
outdoors_name = 'no'  ## 'yes' 'none' 'other'
provider_type = 'RPi3'   ## 'REST API' 
data_quality = 99

#################################################
#################################################

def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time laps in seconds
   dt : datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt == None : dt = datetime.now()
   seconds = (dt - dt.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + timedelta(0,rounding-seconds,-dt.microsecond)

#################################################
#################################################

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])
	
# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])
			
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
	
#sensor = Adafruit_DHT.DHT22
pin = ''

# Try to grab a sensor reading.  Use the read_retry method which will retry up
now1 = datetime.now()
utc1 = datetime.utcnow()
nowsecs = time.mktime(now1.timetuple())
ram_time = nowsecs % (1.001 * (60 * 3))
ram_time_percent = nowsecs % (0.999 * (60 * 12))
disk_time = nowsecs % (1.001 * (60 * 60 * 12))
disk_time_percent = nowsecs % (0.999 * (60 * 60 * 24 * 7))
cpu_tempA = getCPUtemperature()
cpu_use = psutil.cpu_percent()
ram = psutil.virtual_memory()
ram_total = None
ram_used = None
ram_free = None
ram_percent_used = None
if ram_time <= 60 or cpu_use > 80.0 or cpu_tempA > 57.5:
    ram_total = ram.total / 2**20       # MiB.
    ram_used = ram.used / 2**20
    ram_free = ram.free / 2**20
if ram_time_percent <= 60:
    ram_percent_used = ram.percent
disk = psutil.disk_usage('/')
disk_total = None
disk_used = None
disk_remaining = None
disk_percentage = None
if disk_time <= 60:
    disk_total = disk.total / 2**30     # GiB.
    disk_used = disk.used / 2**30
    disk_remaining = disk.free / 2**30
if disk_time_percent <= 60:
    disk_percentage = disk.percent
cpu_tempB = get_cpu_temperature()
cpu_temp = mean([float(cpu_tempA), cpu_tempB])
utc2 = datetime.utcnow()
offset_utc = str(roundTime(now1,roundTo=30*60) - roundTime(utc1,roundTo=30*60))
duration = (utc2-utc1)
duration2 = (float(duration.microseconds) / 10**6) + duration.seconds + (((duration.days * 24) * 60) * 60)


#################################################
#################################################

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!

try:
    connection = lite.connect('freyr.db', isolation_level=None)
    cursor = connection.cursor()
    
    #################################################
    # Outdoors
    ## ID (auto)
    ## name (none, outdoor, indoor, other)  
    cursor.execute("CREATE TABLE IF NOT EXISTS outdoors(id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("SELECT max(id) FROM outdoors WHERE name LIKE ?", ([outdoors_name]))
    outdoors_id = cursor.fetchone()[0]
    if outdoors_id is None:
        cursor.execute("INSERT INTO outdoors(name) VALUES (?)", ([outdoors_name]))
        cursor.execute('SELECT max(id) FROM outdoors')
        outdoors_id = cursor.fetchone()[0]
    # print '|' + str(outdoors_id) + 'out'
    
    #################################################
    # Data Quality
    ## ID (auto)
    ## name (none, fine, maverick, invalid)  
    cursor.execute("CREATE TABLE IF NOT EXISTS data_quality(id INTEGER PRIMARY KEY, name TEXT)")

    #################################################
    # Provider Types
    ## ID (auto)
    ## Type (REST API, RPi3, RPi0)  
    cursor.execute("CREATE TABLE IF NOT EXISTS provider_types(id INTEGER PRIMARY KEY, type TEXT)")
    cursor.execute("SELECT max(id) FROM provider_types WHERE type LIKE ?", ([provider_type]))
    provider_type_id = cursor.fetchone()[0]
    if provider_type_id is None:
        cursor.execute("INSERT INTO provider_types(type) VALUES (?)", ([provider_type]))
        cursor.execute('SELECT max(id) FROM provider_types')
        provider_type_id = cursor.fetchone()[0]
    # print '|' + str(provider_type_id) + 'provider_type_id'

    #################################################
    # Periphery Types
    ## ID (auto)
    ## Type (Sensor, Motor, LED, ...)   
    cursor.execute("CREATE TABLE IF NOT EXISTS periphery_types(id INTEGER PRIMARY KEY, type TEXT)")
    cursor.execute("SELECT max(id) FROM periphery_types WHERE type LIKE ?", ([periphery_type]))
    periphery_type_id = cursor.fetchone()[0]
    if periphery_type_id is None:
        cursor.execute("INSERT INTO periphery_types(type) VALUES (?)", ([periphery_type]))
        cursor.execute('SELECT max(id) FROM periphery_types')
        periphery_type_id = cursor.fetchone()[0]
    # print '|' + str(periphery_type_id) + 'periphery_type'

    #################################################
    # Location
    ## ID (auto)
    ## lat
    ## long
    ## outdoors (ID)
    ## description (in/out, garden, etc.)
    #location_id
    cursor.execute("CREATE TABLE IF NOT EXISTS location(id INTEGER PRIMARY KEY, lat REAL, long REAL, outdoors INTEGER, description TEXT)")
    cursor.execute("SELECT max(id) FROM location WHERE lat = ? AND long = ? AND outdoors = ? AND description LIKE ?", ([loc_lat, loc_long, outdoors_id, loc_description]))
    location_id = cursor.fetchone()[0]
    if location_id is None:
        cursor.execute("INSERT INTO location(lat, long, outdoors, description) VALUES (?, ?, ?, ?)", ([loc_lat, loc_long, outdoors_id, loc_description]))
        cursor.execute('SELECT max(id) FROM location')
        location_id = cursor.fetchone()[0]
    # print '|' + str(location_id) + 'location'

    #################################################
    # Source
    ## ID (auto)
    ## name
    ## location (id)
    ## provider (device / api)
    ## description
    cursor.execute("CREATE TABLE IF NOT EXISTS source(id INTEGER PRIMARY KEY, name TEXT, location INTEGER, provider_type INTEGER, description TEXT)")
    cursor.execute("SELECT max(id) FROM source WHERE name = ? AND location = ? AND provider_type LIKE ? AND description LIKE ?", ([source_name, location_id, provider_type_id, source_description]))
    source_id = cursor.fetchone()[0]
    if source_id is None:
        cursor.execute("INSERT INTO source(name, location, provider_type, description) VALUES (?, ?, ?, ?)", ([source_name, location_id, provider_type_id, source_description]))
        cursor.execute('SELECT max(id) FROM source')
        source_id = cursor.fetchone()[0]
    # print '|' + str(source_id) + 'source'
	
    #################################################
    # Peripheries
    ## ID (auto)
    ## name 
    ## type 
    ## description (i.e. readings)
    #periphery_id
    cursor.execute("CREATE TABLE IF NOT EXISTS periphery(id INTEGER PRIMARY KEY, name TEXT, periphery_type INTEGER, description TEXT, gpio TEXT)") 
    cursor.execute("SELECT max(id) FROM periphery WHERE name = ? AND periphery_type = ? AND description LIKE ? AND gpio = ?", ([periphery_name, periphery_type_id, periphery_description, pin]))
    periphery_id = cursor.fetchone()[0]
    if periphery_id is None:
        cursor.execute("INSERT INTO periphery(name, periphery_type, description, gpio) VALUES (?, ?, ?, ?)", ([periphery_name, periphery_type_id, periphery_description, pin]))
        cursor.execute('SELECT max(id) FROM periphery')
        periphery_id = cursor.fetchone()[0]
    # print '|' + str(periphery_id) + 'periphery'
	
    #################################################
    # Periphery Device
    ## ID (auto)
    ## Periphery Type (ID)
    ## description (i.e. readings)
    #sensor_id
    cursor.execute("CREATE TABLE IF NOT EXISTS periphery_device(id INTEGER PRIMARY KEY, periphery INTEGER, description TEXT)")    
    cursor.execute("SELECT max(id) FROM periphery_device WHERE periphery = ? AND description LIKE ?", ([periphery_id, periphery_device_description]))
    sensor_id = cursor.fetchone()[0]
    if sensor_id is None:
        cursor.execute("INSERT INTO periphery_device (periphery, description) VALUES (?, ?)", ([periphery_id, periphery_device_description]))
        cursor.execute('SELECT max(id) FROM periphery_device')
        sensor_id = cursor.fetchone()[0]
    # print '|' + str(sensor_id) + 'sensor'
	
    #################################################
    # Measures
    ## ID (auto)
    ## absolute_min
    ## absolute_max
    ## name (i.e Celsious)
    ## symbol (i.e. °C)
    ## type_full (i.e. temperature)
    ## type_abbr (i.e. temp)
    #measure_id
    cursor.execute("CREATE TABLE IF NOT EXISTS measures(id INTEGER PRIMARY KEY, name TEXT, sign INTEGER, type_full TEXT, type_abbr TEXT, absolute_min REAL, absolute_max REAL)")    
    
    measure_name = 'celsius'
    measure_sign = u'\u2103' #.encode('utf8')  #'°C'
    measure_type_full = 'temperature'
    measure_type_abbr = 'temp'
    measure_absolute_min = (273.15 * (-1))
    measure_absolute_max = None
    cursor.execute("SELECT max(id) FROM measures WHERE (name LIKE ? OR sign LIKE ?) AND type_full LIKE ? AND (type_abbr LIKE ? OR absolute_min = ? OR absolute_max = ?)", ([measure_name, measure_sign, measure_type_full, measure_type_abbr, measure_absolute_min, measure_absolute_max]))
    temp_measure_id = cursor.fetchone()[0]
    if temp_measure_id is None:
        cursor.execute("INSERT INTO measures(name, sign, type_full, type_abbr, absolute_min, absolute_max) VALUES (?, ?, ?, ?, ?, ?)", ([measure_name, measure_sign, measure_type_full, measure_type_abbr, measure_absolute_min, measure_absolute_max]))
        cursor.execute('SELECT max(id) FROM measures WHERE type_abbr LIKE ?', ([measure_type_abbr]))
        temp_measure_id = cursor.fetchone()[0]
    # print '|' + str(temp_measure_id) + '°C'
	
    measure_name = 'percent'
    measure_sign = '%'
    measure_type_full = 'Used Capacity'
    measure_type_abbr = 'usage'
    measure_absolute_min = 0.0
    measure_absolute_max = 100.0
    cursor.execute("SELECT max(id) FROM measures WHERE (name LIKE ? OR sign LIKE ?) AND type_full LIKE ? AND (type_abbr LIKE ? OR absolute_min = ? OR absolute_max = ?)", (measure_name, measure_sign, measure_type_full, measure_type_abbr, measure_absolute_min, measure_absolute_max))
    percent_measure_id = cursor.fetchone()[0]
    if percent_measure_id is None:
        cursor.execute("INSERT INTO measures(name, sign, type_full, type_abbr, absolute_min, absolute_max) VALUES (?, ?, ?, ?, ?, ?)", (measure_name, measure_sign, measure_type_full, measure_type_abbr, measure_absolute_min, measure_absolute_max))
        cursor.execute('SELECT max(id) FROM measures WHERE type_abbr LIKE ?', ([measure_type_abbr]))
        percent_measure_id = cursor.fetchone()[0]
    # print '|' + str(percent_measure_id) + '%'
	
    measure_name = 'Mega Byte'
    measure_sign = 'MB'
    measure_type_full = 'Memory'
    measure_type_abbr = 'mem'
    measure_absolute_min = 0.0
    measure_absolute_max = ram_total
    cursor.execute("SELECT max(id) FROM measures WHERE (name LIKE ? OR sign LIKE ?) AND type_full LIKE ? AND (type_abbr LIKE ? OR absolute_min = ? OR absolute_max = ?)", (measure_name, measure_sign, measure_type_full, measure_type_abbr, measure_absolute_min, measure_absolute_max))
    mb_measure_id = cursor.fetchone()[0]
    if mb_measure_id is None:
        cursor.execute("INSERT INTO measures(name, sign, type_full, type_abbr, absolute_min, absolute_max) VALUES (?, ?, ?, ?, ?, ?)", (measure_name, measure_sign, measure_type_full, measure_type_abbr, measure_absolute_min, measure_absolute_max))
        cursor.execute('SELECT max(id) FROM measures WHERE type_abbr LIKE ?', ([measure_type_abbr]))
        mb_measure_id = cursor.fetchone()[0]
    # print '|' + str(mb_measure_id) + 'MB'
	
    measure_name = 'Giga Byte'
    measure_sign = 'GB'
    measure_type_full = 'Memory'
    measure_type_abbr = 'mem'
    measure_absolute_min = 0.0
    measure_absolute_max = disk_total
    cursor.execute("SELECT max(id) FROM measures WHERE (name LIKE ? OR sign LIKE ?) AND type_full LIKE ? AND (type_abbr LIKE ? OR absolute_min = ? OR absolute_max = ?)", (measure_name, measure_sign, measure_type_full, measure_type_abbr, measure_absolute_min, measure_absolute_max))
    gb_measure_id = cursor.fetchone()[0]
    if gb_measure_id is None:
        cursor.execute("INSERT INTO measures(name, sign, type_full, type_abbr, absolute_min, absolute_max) VALUES (?, ?, ?, ?, ?, ?)", (measure_name, measure_sign, measure_type_full, measure_type_abbr, measure_absolute_min, measure_absolute_max))
        cursor.execute('SELECT max(id) FROM measures WHERE type_abbr LIKE ?', ([measure_type_abbr]))
        gb_measure_id = cursor.fetchone()[0]
    # print '|' + str(gb_measure_id) + 'GB'
	
    #################################################
    # measure_target_types
    ## ID (auto)
    ## measure_target_type
    cursor.execute("CREATE TABLE IF NOT EXISTS measure_target_types(id INTEGER PRIMARY KEY, measure_target_type TEXT)")
    cursor.execute("SELECT max(id) FROM measure_target_types WHERE measure_target_type LIKE ?", ([CPU_measure_target_type]))
    CPU_target_id = cursor.fetchone()[0]
    if CPU_target_id is None:
        cursor.execute("INSERT INTO measure_target_types(measure_target_type) VALUES (?)", ([CPU_measure_target_type]))
        cursor.execute('SELECT max(id) FROM measure_target_types')
        CPU_target_id = cursor.fetchone()[0]
    # print '|' + str(CPU_target_id) + 'CPU'
	
    cursor.execute("SELECT max(id) FROM measure_target_types WHERE measure_target_type LIKE ?", ([RAM_measure_target_type]))
    RAM_target_id = cursor.fetchone()[0]
    if RAM_target_id is None:
        cursor.execute("INSERT INTO measure_target_types(measure_target_type) VALUES (?)", ([RAM_measure_target_type]))
        cursor.execute('SELECT max(id) FROM measure_target_types')
        RAM_target_id = cursor.fetchone()[0]
    #print '|' + str(RAM_target_id) + 'RAM'
	
    cursor.execute("SELECT max(id) FROM measure_target_types WHERE measure_target_type LIKE ?", ([Disk_measure_target_type]))
    Disk_target_id = cursor.fetchone()[0] 
    if Disk_target_id is None:
        cursor.execute("INSERT INTO measure_target_types(measure_target_type) VALUES (?)", ([Disk_measure_target_type]))
        cursor.execute('SELECT max(id) FROM measure_target_types')
        Disk_target_id = cursor.fetchone()[0]
    # print '|' + str(Disk_target_id) + 'DISK'
	
    #################################################
    # measure_target
    ## ID (auto)
    ## name
    ## description (additional information)
    cursor.execute("CREATE TABLE IF NOT EXISTS measure_targets(id INTEGER PRIMARY KEY, measure_target_name TEXT, measure_target_type INTEGER, measure_target_description TEXT)")

    cursor.execute("SELECT max(id) FROM measure_targets WHERE measure_target_name = ? AND measure_target_type = ? AND measure_target_description = ?", ([measure_target_name, CPU_target_id, measure_target_description]))
    CPU_measure_target_id = cursor.fetchone()[0]
    if CPU_measure_target_id is None:
        cursor.execute("INSERT INTO measure_targets(measure_target_name, measure_target_type, measure_target_description) VALUES (?, ?, ?)", ([measure_target_name, CPU_target_id, measure_target_description]))
        cursor.execute('SELECT max(id) FROM measure_targets')
        CPU_measure_target_id = cursor.fetchone()[0]
    # print '|' + str(CPU_measure_target_id) + 'CPU'
	
    cursor.execute("SELECT max(id) FROM measure_targets WHERE measure_target_name = ? AND measure_target_type = ? AND measure_target_description = ?", ([measure_target_name, RAM_target_id, measure_target_description]))
    RAM_measure_target_id = cursor.fetchone()[0]
    if RAM_measure_target_id is None:
        cursor.execute("INSERT INTO measure_targets(measure_target_name, measure_target_type, measure_target_description) VALUES (?, ?, ?)", ([measure_target_name, RAM_target_id, measure_target_description]))
        cursor.execute('SELECT max(id) FROM measure_targets')
        RAM_measure_target_id = cursor.fetchone()[0]
    # print '|' + str(RAM_measure_target_id) + 'RAM'
	
    cursor.execute("SELECT max(id) FROM measure_targets WHERE measure_target_name = ? AND measure_target_type = ? AND measure_target_description = ?", ([measure_target_name, Disk_target_id, measure_target_description]))
    Disk_measure_target_id = cursor.fetchone()[0]
    if Disk_measure_target_id is None:
        cursor.execute("INSERT INTO measure_targets(measure_target_name, measure_target_type, measure_target_description) VALUES (?, ?, ?)", ([measure_target_name, Disk_target_id, measure_target_description]))
        cursor.execute('SELECT max(id) FROM measure_targets')
        Disk_measure_target_id = cursor.fetchone()[0]
    # print '|' + str(Disk_measure_target_id) + 'Disk'
	
    #################################################
    # read_log
    ## ID (auto)
    ## sensor (ID)
    ## source (ID)
    ## utc_start
    ## utc_end
    ## timezone
    ## duration2 (secs)    
    cursor.execute("CREATE TABLE IF NOT EXISTS read_log(id INTEGER PRIMARY KEY, sensor INTEGER, source INTEGER, utc_start TIMESTAMP, utc_end TIMESTAMP, offset_utc TIMESTAMP, duration_sec REAL)")
    if cpu_tempA is not None or cpu_tempB is not None or cpu_use is not None or disk_percentage is not None or ram_used is not None or disk_used is not None or ram_percent_used is not None:
        cursor.execute("INSERT INTO read_log(sensor, source, utc_start, utc_end, offset_utc, duration_sec) VALUES (?, ?, ?, ?, ?, ?)", (sensor_id, source_id, utc1, utc2, offset_utc, duration2))
        cursor.execute('SELECT max(id) FROM read_log')
        new_log = cursor.fetchone()[0]
    # print str(new_log) + 'log'
	
    #################################################
    # Readings
    ## ID (auto)
    ## measure (ID)
    ## reading (from sensor)
    ## read_log (ID)
    cursor.execute("CREATE TABLE IF NOT EXISTS readings(id INTEGER PRIMARY KEY, measure INTEGER, reading REAL, read_log INTEGER, data_quality INTEGER, measure_target_id INTEGER)")
	
    if cpu_temp is not None:
        cursor.execute("INSERT INTO readings(measure, reading, read_log, data_quality, measure_target) VALUES (?, ?, ?, ?, ?)", (temp_measure_id, cpu_temp, new_log, data_quality, CPU_measure_target_id))
    # print str(cpu_tempA) + 'cpu_tempA'
	
    if cpu_use is not None:
        cursor.execute("INSERT INTO readings(measure, reading, read_log, data_quality, measure_target) VALUES (?, ?, ?, ?, ?)", (percent_measure_id, cpu_use, new_log, data_quality, CPU_measure_target_id))
    # print str(cpu_use) + 'cpu_use'
	
    if disk_percentage is not None:
        cursor.execute("INSERT INTO readings(measure, reading, read_log, data_quality, measure_target) VALUES (?, ?, ?, ?, ?)", (percent_measure_id, disk_percentage, new_log, data_quality, Disk_measure_target_id))
    # print str(disk_percentage) + 'disk_percentage'
	
    if ram_used is not None:
        cursor.execute("INSERT INTO readings(measure, reading, read_log, data_quality, measure_target) VALUES (?, ?, ?, ?, ?)", (mb_measure_id, ram_used, new_log, data_quality, RAM_measure_target_id))
    # print str(ram_used) + 'ram_used'

    if ram_percent_used is not None:
        cursor.execute("INSERT INTO readings(measure, reading, read_log, data_quality, measure_target) VALUES (?, ?, ?, ?, ?)", (percent_measure_id, ram_percent_used, new_log, data_quality, RAM_measure_target_id))
    # print str(ram_used) + 'ram_used'
	
    if disk_used is not None:
        cursor.execute("INSERT INTO readings(measure, reading, read_log, data_quality, measure_target) VALUES (?, ?, ?, ?, ?)", (gb_measure_id, disk_used, new_log, data_quality, Disk_measure_target_id))
    # print str(disk_used) + 'disk_used'
		
except lite.Error, e:    
    
    ##print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if connection:
        connection.close() 
