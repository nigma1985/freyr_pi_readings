import subprocess
from module.config import ConfigSectionMapAdv
from module.getOptions import findItm

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
