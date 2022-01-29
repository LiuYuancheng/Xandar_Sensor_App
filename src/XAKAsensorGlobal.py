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

print("XAKAsensorGlobal: Current working directory is : %s" %str(os.getcwd()))

dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = 'Packet_Parser_PQC_v0.1'


# Application name and version. setting
APP_NAME = 'XAKA People Counting Sensor_v2.1'

#UI window ICON.
ICON_PATH = "".join([dirpath, "\\firmwSign\\singtelIcon.ico"])
BGPNG_PATH = "".join([dirpath, "\\firmwSign\\TopView.png"])

RGTCP_PORT = 5006   # port for sensor registration request.
# Sensor registration server choice:
RG_SERVER_CHOICE = {
    "LocalDefault [127.0.0.1]"  : ('127.0.0.1', RGTCP_PORT),
    "Server_1 [192.168.0.100]"  : ('192.168.0.100', RGTCP_PORT),
}

#-----------------------------------------------------------------------------
# Set the global reference here.
iChartPanel = None      # History chart panel
iMapPanel = None        # Monitor area map panel
iDetailPanel = None     # Detail informaiton display panel
iMainFrame = None       # Program main frame
