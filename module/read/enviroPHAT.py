from envirophat import light, motion, weather, analog, leds
## please install https://github.com/pimoroni/enviro-phat
## documentation is here: http://docs.pimoroni.com/envirophat/

def getRGB():
    ## returns list: Red, Green, Blue
    ## values 0 - 255
    return light.rgb()

def getLight():
    return light.light()

def getRaw():
    ## returns list: Red, Green, Blue, Clear (Light)
    ## values 0 - Clear // RGB = value / clear * 255
    return light.raw()


def setLedOn():
    leds.on()

def setLedOff():
    leds.off()

def getLedOn():
    ## returns true if on
    return leds.is_on()

def getLedOff():
    ## returns true if off
    return leds.is_off()

def getLedStatus():
    ## returns true if on and false if off
    if leds.is_off():
        return False
    elif leds.is_on():
        return True
    else:
        return None

def getTemp():
    return weather.temperature()

def getPrss():
    return weather.pressure()

def getAltd(qnh = None):
    if qnh is None:
        qnh = 1020
    return weather.altitude(qnh)

def getWeatherUpdate():
    return weather.update()

## No analog reading interpreted
# analog.read(channel=0, programmable_gain=None, samples_per_second=1600)
# analog.read_all()
# analog.available()

def getMagn():
    return motion.magnetometer()

def getAccl():
    return motion.accelerometer()

def getHead():
    return motion.heading()

def getRawHead():
    return motion.raw_heading()

def getMotionUpdate():
    return motion.update()
