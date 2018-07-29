import sys, re
from os.path import isfile
from module.config import ConfigSectionMapAdv
from module.timeTool import csvTimeFormat
import module.getOptions as opt
import unicodecsv as csv

def stdLine(
    value,
    pin,
    # time
    utc_1,
    utc_2,
    offsetutc,
    duration_sec,
    # location
    outdoors_name,  ##'no'  ## 'yes' 'none' 'other'
    loc_lat,  ##53.304130
    loc_long,  ##9.706472
    loc_description,  ##'test indoor'
    # source / provider
    provider_type,  ##'RPi3'   ## 'REST API'
    source_name, ##'FreyrTST 1'
    source_description,  ##'Test RPi3 -
    # periphery
    periphery_name,  ##'Raspberry Pi 3'
    periphery_type,  ##'System'
    periphery_description,  ##'Hardware'
    periphery_device_description,  ##'tst'
    # measure
    measure_name,
    measure_sign,
    measure_type_full,
    measure_type_abbr,
    measure_absolute_min,
    measure_absolute_max,
    measure_target_type,
    measure_target_name,  ##'System' ## 'yes' 'none' 'other'
    measure_target_description,  ##'Monitoring Hardware'
    # QA
    data_quality  ##99
):
    return [value, pin, utc_1, utc_2, offsetutc, duration_sec,outdoors_name, loc_lat, loc_long, loc_description, provider_type, source_name, source_description, periphery_type, periphery_name, periphery_description, periphery_device_description, measure_name, measure_sign, measure_type_full, measure_type_abbr, measure_absolute_min, measure_absolute_max, measure_target_type, measure_target_name, measure_target_description, data_quality]

def headLine(
    _value = "value",
    _pin = "pin",
    # time
    _utc_1 = "utc_1",
    _utc_2 = "utc_2",
    _offsetutc = "offsetutc",
    _duration_sec = "duration_sec",
    # location
    _outdoors_name = "outdoors_name",  ##'no'  ## 'yes' 'none' 'other'
    _loc_lat = "loc_lat",  ##53.304130
    _loc_long = "loc_long",  ##9.706472
    _loc_description = "loc_description",  ##'test indoor'
    # source / provider
    _provider_type = "provider_type",  ##'RPi3'   ## 'REST API'
    _source_name = "source_name", ##'FreyrTST 1'
    _source_description = "source_description",  ##'Test RPi3 -
    # periphery
    _periphery_name = "periphery_name",  ##'Raspberry Pi 3'
    _periphery_type = "periphery_type",  ##'System'
    _periphery_description = "periphery_description",  ##'Hardware'
    _periphery_device_description = "periphery_device_description",  ##'tst'
    # measure
    _measure_name = "measure_name",
    _measure_sign = "measure_sign",
    _measure_type_full = "measure_type_full",
    _measure_type_abbr = "measure_type_abbr",
    _measure_absolute_min = "measure_absolute_min",
    _measure_absolute_max = "measure_absolute_max",
    _measure_target_type = "measure_target_type",
    _measure_target_name = "measure_target_name",  ##'System' ## 'yes' 'none' 'other'
    _measure_target_description = "measure_target_description",  ##'Monitoring Hardware'
    # QA
    _data_quality = "data_quality"  ##99
):
    return stdLine(
        value = _value, pin = _pin,
        utc_1 = _utc_1, utc_2 = _utc_2, offsetutc = _offsetutc, duration_sec = _duration_sec,
        outdoors_name = _outdoors_name, loc_lat = _loc_lat, loc_long = _loc_long, loc_description = _loc_description,
        provider_type = _provider_type, source_name = _source_name, source_description = _source_description,
        periphery_name = _periphery_name, periphery_type = _periphery_type, periphery_description = _periphery_description, periphery_device_description = _periphery_device_description,
        measure_name = _measure_name, measure_sign = _measure_sign, measure_type_full = _measure_type_full, measure_type_abbr = _measure_type_abbr, measure_absolute_min = _measure_absolute_min, measure_absolute_max = _measure_absolute_max, measure_target_type = _measure_target_type, measure_target_name = _measure_target_name, measure_target_description = _measure_target_description,
        data_quality = _data_quality
    )

def defaultFileName(host = None):
    if host is None:
        host = ConfigSectionMapAdv(option = 'source_name')
    return "out/FREYR_" + csvTimeFormat() + "_" + host + ".csv"

def csvName(user = None, options = sys.argv):
   regex = "^(out\/FREYR\_....-..-..\_....\_" + user + "\.csv)"
   if user is None:
       user = ConfigSectionMapAdv(option = 'source_name')
   file = None
   if type(options) == list:
       for opt in options:
           if opt.checkArgv(opt, regex):
              file = opt
   else:
       if opt.checkArgv(options, regex):
           file = options
   if file is None:
       file = defaultFileName(user)
   return file

def initiateFile(x = None):
    if x is None:
        raise "ERROR: No file!"
    elif not isfile(x):
        with open(x, 'ab') as csvfile:
            y = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_NONNUMERIC)
            y.writerow(headLine())
    return

def writeRow(row = None, csvFile = None):
    if not isfile(csvFile):
        if csvFile is None:
            csvFile = defaultFileName()
        initiateFile(csvFile)
    with open(csvFile, 'ab') as csvfile:
        y = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_NONNUMERIC)
        if (row is not None) and (type(row) != list):
            raise "ERROR: Missing data!"
        elif row is None:
            y.writerow(headLine())
        else:
            y.writerow(row)
    return
