import os

sourceFolder = "/home/pi/PiHead/LightSensor/"
destFolder = "/opt/lightsensor/"
files=["lightsensor_default_env.sh", "lightsensor_env.sh", "lightsensor.service", "service_lightsensor.py"]

if os.path.isdir(destFolder):
    os.system("sudo chmod -R a+rw " + destFolder)
    os.system("sudo rm -rf " + destFolder + "*")
    bNew = False
else:
    os.system("sudo mkdir -p "+ destFolder)
    os.system("sudo chmod a+rw " + destFolder)
    bNew = True
    
for i in files:
    os.system("sudo cp -f " + sourceFolder + files[i] + " " + destFolder)
    os.system("sudo chmod a+rwx " + destFolder + files[i])

os.system("sudo cp -f " + destFolder + "lightsensor.service /etc/systemd/system")

if bNew == True:
    os.system("sudo systemctl enable lightsensor.service")
    os.system("sudo systemctl start lightsensor.service")
else:
    os.system("sudo systemctl daemon-reload")
    os.system("sudo systemctl restart lightsensor.service")
