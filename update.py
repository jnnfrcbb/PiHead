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

def updateRepo(userName,repoName):
    updated = 0
    repoAddress = "https://github.com/" + userName + "/" + repoName
    if os.path.isdir(repoName):
        os.system("cd " + repoName)
        url = "git pull " + repoAddress
        updated = os.system(url)
    else:
        url = "git clone " + repoAddress
        updated = os.system(url)
    return updated

c=0
while c < 5:
    if internet():
        p = updateRepo("jnnfrcbb","PiHead")
        print (p)
        if "up-to-date" not in p:
            os.system("reboot")
    else:
        time.sleep(30)
    c=c+1

exit

