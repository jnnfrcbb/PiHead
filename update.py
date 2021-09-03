import os
import socket
import time

def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False

def updateRepo(repoAddress):
    updated = 0
    if os.path.isdir(repoAddress):
        url = "git pull https://github.com/" + repoAddress
        updated = os.system(url)
    else:
        url = "git clone https://github.com/" + repoAddress
        updated = os.system(url)
    return updated

if internet():
    p = updateRepo("jnnfrcbb/PiHead")
    print (p)
    #os.system("reboot")
else:
    time.sleep(30)

