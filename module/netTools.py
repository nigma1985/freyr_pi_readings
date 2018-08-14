import subprocess
from random import *
from module.config import ConfigSectionMapAdv
from module.getOptions import findItm

def ping_singlehost(host = None, tries = None):
    if host is None:
        host = ConfigSectionMapAdv(option = 'source_name')
    if tries is None or type(tries) != numbers:
        tries = randint(1, 10)
    try:
        output = subprocess.check_output("ping -{} {} {}".format('n' if platform.system().lower()=="windows" else 'c', tries, host), shell=True)
    except Exception, e:
        return False
    return True

def ping_host(hosts = None, meta_trys = None):
    if hosts is None:
        hosts = ConfigSectionMapAdv(option = 'source_name')
    if meta_trys is None or type(meta_trys) != numbers:
        meta_trys = randint(3, 10)
    if isinstance(hosts, str):
        return ping_singlehost(host = hosts, trys = meta_tries)
    elif isinstance(hosts, (list, tuple)):
        i = 0 # result to be returned
        j = meta_tries # number tries
        k = 0 # random number of pings (lower j)
        l = 0 # number of hosts pinged
        m = 0
        hosts = sample(hosts, j) # take random sample of hosts, shuffle them
        # hosts = shuffle(hosts) # take random sample of hosts, shuffle them
        for h in hosts: # loop host list
            m = m + 1
            k = 0
            if (random() ** 2) >= (m / len(hosts)):
                k = randint(0,j)
            if m == len(hosts):
                k = j
            # k = randint(0,y)
            # print "numb of pings now: " + str(k)
            if k > 0:
                if ping_singlehost(host = h, trys = k) == False:
                    # print h + " : " + str(k) + "x"
                    i = i + 1
                j = j - k
                l = l + 1
        # print 1.0 * (i / l)
        return .5 > 1.0 * (i / l) # more then half of hosts = no connection
    else:
        return None


def scp(file = "", user = None, host = None, path = "~/in/"):
    if (file is None) or (file == ""):
        raise "No file"
    if user is None:
        user = ConfigSectionMapAdv(option = 'source_name')
    if host is None:
        host = ConfigSectionMapAdv(option = 'user')

    cmd = "scp {} {}@{}:{}".format(file, user, host, path)
    response = subprocess.call(cmd, shell=True)
    return response == 0
