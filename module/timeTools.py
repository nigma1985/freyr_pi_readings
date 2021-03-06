from datetime import datetime
from datetime import timedelta
import time


#################################################
###  Tools for time management                ###
#################################################

def csvTimeFormat():
    tst = datetime.utcnow()
    return str(tst.strftime("%Y-%m-%d_%H%M"))

def now():
    return datetime.now()

def utcnow():
    return datetime.utcnow()

def mktime(dt = datetime.now()):
    return time.mktime(dt.timetuple())

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

def start():
    now = datetime.now()
    return now, datetime.utcnow(), time.mktime(now.timetuple())

def end(now1, utc1):
    if None in [now1, utc1]:
        startBuffer = start()
    if now1 is None:
        now1 = startBuffer[0]
    if utc1 is None:
        utc1 = startBuffer[1]
    utc2 = datetime.utcnow()
    duration = (utc2-utc1)
    return utc2, str(roundTime(now1,roundTo=30*60) - roundTime(utc1,roundTo=30*60)), duration, (float(duration.microseconds) / 10**6) + duration.seconds + (((duration.days * 24) * 60) * 60)

def sleeper(timer = None):
    time.sleep(timer)
