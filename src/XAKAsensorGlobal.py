#-----------------------------------------------------------------------------
# Name:        XAKAsensorGlobal.py
#
# Purpose:     This module is used as a local config file to set global variables
#              which will be used in the other modules.
# Author:      Yuancheng Liu
#
# Created:     2019/07/05 [rebuilt on 29/01/2022]
# version:     v_2.1
# Copyright:   NUS – Singtel Cyber Security Research & Development Laboratory
# License:     YC @ NUS
#-----------------------------------------------------------------------------

import os
import platform

print("Current working directory is : %s" % str(os.getcwd()))
dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)

# Application name and version. setting
APP_NAME = 'XAKA People Counting Sensor_v2.1'
# User need to change below part if the sensor is plugged in different USB port.
DE_COMM = 'COM3' if platform.system() == 'Windows' else '/dev/ttyUSB0'

#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = 'img'
ICON_PATH = os.path.join(dirpath, IMG_FD, 'singtelIcon.ico')
BGPNG_PATH = os.path.join(dirpath, IMG_FD, 'TopView.png')

RGTCP_PORT = 5006   # port for sensor registration request.
# Sensor registration server choice:
RG_SERVER_CHOICE = {
    "LocalDefault [127.0.0.1]": ('127.0.0.1', RGTCP_PORT),
    "Server_1 [192.168.0.100]": ('192.168.0.100', RGTCP_PORT),
}
BUFFER_SIZE = 4096

#-----------------------------------------------------------------------------
# Set the global reference here.
iChartPanel = None      # History chart panel
iMapPanel = None        # Monitored indoor area map panel
iDetailPanel = None     # Detail informaiton display panel
iMainFrame = None       # Program main frame

#-----------------------------------------------------------------------------
# Set the global paramter/flag here.
gSimulationMode = True
