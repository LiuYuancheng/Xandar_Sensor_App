#-----------------------------------------------------------------------------
# Name:        XAKAsensorGlobal.py
#
# Purpose:     This module is used set the Local config file as global value 
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

print("XAKAsensorGlobal: Current working directory is : %s" %str(os.getcwd()))

dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = 'Packet_Parser_PQC_v0.1'

# Application name and version. setting
APP_NAME = 'XAKA People Counting Sensor_v2.1'

#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = 'img'
ICON_PATH = os.path.join(dirpath, IMG_FD, 'singtelIcon.ico')
BGPNG_PATH = os.path.join(dirpath, IMG_FD, 'TopView.png')
DE_COMM = 'COM3' if platform.system() == 'Windows' else '/dev/ttyUSB0'

RGTCP_PORT = 5006   # port for sensor registration request.
# Sensor registration server choice:
RG_SERVER_CHOICE = {
    "LocalDefault [127.0.0.1]"  : ('127.0.0.1', RGTCP_PORT),
    "Server_1 [192.168.0.100]"  : ('192.168.0.100', RGTCP_PORT),
}

# Server ip and port for connection: 
LOCAL_IP = '127.0.0.1'
SITCP_PORT = 5005   # port for firmware sign request.
RGTCP_PORT = 5006   # port for sensor registration request.

# Firmware sign server choice:
SI_SERVER_CHOICE = {
    "LocalDefault [127.0.0.1]"  : ('127.0.0.1', SITCP_PORT),
    "Server_1 [192.168.0.100]"  : ('192.168.0.100', SITCP_PORT),
    "Server_2 [192.168.0.101]"  : ('192.168.0.101', SITCP_PORT)
}

#-----------------------------------------------------------------------------
# Set the global reference here.
iChartPanel = None      # History chart panel
iMapPanel = None        # Monitor area map panel
iDetailPanel = None     # Detail informaiton display panel
iMainFrame = None       # Program main frame

#-----------------------------------------------------------------------------
# Set the global paramter/flag here.
gSimulationMode = True