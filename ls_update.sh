#!/bin/bash

sudo chmod -R a+rw /opt/lightsensor/
rm -rf /opt/lightsensor/*

sudo cp /LightSensor/lightsensor_default_env.sh /opt/lightsensor/
sudo cp /LightSensor/lightsensor_env.sh /opt/lightsensor/
sudo cp /LightSensor/service_lightsensor.py /opt/lightsensor/
sudo cp /LightSensor/lightsensor.service /etc/systemd/system

sudo chmod a+rwx /opt/lightsensor/service_lightsensor.py
sudo chmod a+rwx /opt/lightsensor/lightsensor_default_env.sh
sudo chmod a+rwx /opt/lightsensor/lightsensor_env.sh
sudo chmod a+rwx /etc/systemd/system/lightsensor.service

systemctl daemon-reload
systemctl restart lightsensor.service