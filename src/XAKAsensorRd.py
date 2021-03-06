#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        XAKAsensorReader.py
#
# Purpose:     This module is used to read the data from XAKA people counting
#              sensor and show the data in the user interface.(optional functions: 
#              register the sensor to the server, automatically detect the sensor)
#             
# Author:      Yuancheng Liu
#
# Created:     2019/03/27 [rebuilt on 29/01/2022]
# version:     v_2.1
# Copyright:   NUS – Singtel Cyber Security Research & Development Laboratory
# License:     YC @ NUS
#-----------------------------------------------------------------------------

import wx # use wx to build the UI.

#In this project we remove the firmware attestation part.
#import firmwMsgMgr
#import firmwTLSclient as SSLC
import XAKAsensorComm as xcomm
import XAKAsensorGlobal as gv
import XAKAsensorPanel as xsp

PERIODIC = 500 # how many ms the periodic call back
SENSOR_TYPE = 'XKAK_PPL_COUNT' # defualt sensor type.

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class SensorReaderFrame(wx.Frame):
    """ XAKA people counting sensor reader with sensor registration function. """
    def __init__(self, parent, id, title):
        """ Init the UI and all parameters """
        wx.Frame.__init__(self, parent, id, title, size=(500, 360))
        self.SetIcon(wx.Icon(gv.ICON_PATH))
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        gv.iMainFrame = self
        # Init parameters.
        self.activeFlag = True     # whether we active the sensor data reading.
        self.senId = self.version = ''
        self.signature = '44c88023c0a6da30e78e1e699d01436cbf987f06213d15b64e0a972952fbd0a3ec578d33a67d34024e8851b776d7af7999f5f175c896c363ed4a93f6cd104a454eb8a48ab32da07489c1daee6614a45561c8823e462e72ce458a78e3f35f68ae157a027d165eb7dec9c8910af34723a9e14132943a9788bfbdc2c904d2207c6a36e92e647c3b450d14697856c2906f94b122a3a01966d48f72f3b29f8472a24813f471be288522ee68ad7de57ec9551722aa9dafdba991516535e618c8a3a94907ca7a46ff11e27bb254497a306685066a86c34eaa572cbf4ab44eaef0829ff1d6f0490ab8d0dece01cf031eda5a1f2690e8579b4cad5cf650846ed6bd4085db' 
        # Init the UI.
        self.SetSizer(self.buildUISizer())
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Register the connected sensor first.')
        # Init the SSL client to TLS connection.
        #self.sslClient = SSLC.TLS_sslClient(self)  # ssl client to send the sensor signature.
        # Init the message manager.
        #self.msgMgr = firmwMsgMgr.msgMgr(self)  # create the message manager.
        # Init the serial reader
        self.serComm = xcomm.XAKAsensorComm(gv.DE_COMM, simuMd=gv.gSimulationMode) # serial comm handler used to read the sensor data. 
        self.serComm.setSerialComm(searchFlag=True)
        # Init the recall future.
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(PERIODIC)  # every 500 ms
        # Add Close event here.
        self.Bind(wx.EVT_CLOSE, self.OnClose)

#--SensorReaderFrame-----------------------------------------------------------
    def buildUISizer(self):
        """ Init the frame user interface and return the sizer."""
        sizer = wx.BoxSizer(wx.HORIZONTAL)    
        nb = wx.Notebook(self)
        # Set the NoteBook page 1(sensor 1)
        ntbgPage1 = wx.Panel(nb)
        hboxPg1= wx.BoxSizer(wx.HORIZONTAL)
        self.linechart = xsp.PanelChart(ntbgPage1, recNum=60)
        gv.iChartPanel = self.linechart
        hboxPg1.Add(self.linechart, 1)
        hboxPg1.AddSpacer(5)
        self.infoPanel = xsp.PanelBaseInfo(ntbgPage1)
        hboxPg1.Add(self.infoPanel,1)
        ntbgPage1.SetSizer(hboxPg1)
        nb.AddPage(ntbgPage1, "Sensor-1")
        # Set the NoteBook page 2(sensor N)
        ntbgPage2 = xsp.PanelPlaceHolder(nb)
        nb.AddPage(ntbgPage2, "Sensor-2")
        # Set the NoteBook page 3(All sensor information.)
        self.multiInfoPg =xsp.PanelMultInfo(nb)
        nb.AddPage(self.multiInfoPg, "Multi-Info")
        # Set the NoteBook sage 4(Setting)
        self.setupPanel = xsp.PanelSetup(nb)
        nb.AddPage(self.setupPanel, "Setting")
        sizer.Add(nb, 1, wx.EXPAND)
        return sizer

#--SensorReaderFrame-----------------------------------------------------------
    def logtoServer(self, ServerName):
        """ Login to the server and register the sensor."""
        try:
            # Connect to the selected server. 
            ip, port = gv.RG_SERVER_CHOICE[ServerName]
            self.sslClient.connect((ip, port))
            # Send SSL connection request cmd and get response.
            self.sslClient.send(self.msgMgr.dumpMsg(action='CR'))
            dataDict = self.msgMgr.loadMsg(self.sslClient.recv(gv.BUFFER_SIZE))
            if dataDict['act'] == 'HB' and dataDict['lAct'] == 'CR' and dataDict['state']:
                print("SConnetion: Connect to the server succesfully.")
            else:
                print("SConnetion: Connection request denied by server.")
                return
            print("SConnetion: start register to server")
            # Register the sensor.(Temporary hard code the sigature for test.)
            data = (self.senId, SENSOR_TYPE, self.version, self.signature)
            self.sslClient.send(self.msgMgr.dumpMsg(action='RG', dataArgs=data))
            dataDict = self.msgMgr.loadMsg(self.sslClient.recv(gv.BUFFER_SIZE))
            if dataDict['act'] == 'HB' and dataDict['lAct'] == 'RG' and dataDict['state']:
                self.statusbar.SetStatusText("Sensor registration success.")
                self.activeFlag = True
            else:
                self.statusbar.SetStatusText("Sensor registration fail.")
                wx.MessageBox('Sensor registration Fail', 'Caution',
                    wx.OK | wx.ICON_ERROR)
            # Logout after resigtered.
            datab = self.msgMgr.dumpMsg(action='LO')
            self.sslClient.send(datab)
            self.sslClient.close()
        except:
            print("Connect to server fail.")

#--SensorReaderFrame-----------------------------------------------------------
    def periodic(self, event):
        """ Periodic call back: read the data one time and find the correct 
            string can be used.
        """
        self.serComm.fetchSensorData()
        self.dataList = self.serComm.getData()
        # Set sensor ID and version for resigter
        if not (self.senId and self.version):
            self.senId, self.version = self.dataList[0], self.dataList[8]
        if not self.activeFlag: return
        # Update the UI if the sensor registed successfully.
        self.updateUIPanels()


 #--SensorReaderFrame-----------------------------------------------------------
    def sigaSimuInput(self, event):
        """ Pop up and diaglog to input the sigature used for simulation."""
        dlg = wx.TextEntryDialog(self, "Enter the sensor sigature for simualtion", ' ')
        dlg.CentreOnParent()
        if dlg.ShowModal() == wx.ID_OK:
            self.signature=dlg.GetValue()

#--SensorReaderFrame-----------------------------------------------------------
    def updateUIPanels(self):
        """ Update the UI of all the Panels"""
        # Update the sensor detail information frame.
        if gv.iDetailPanel: gv.iDetailPanel.updateDisplay(self.dataList)
        # Update the sensor history line chart.
        self.linechart.appendData(
            list((self.dataList[4], self.dataList[9], self.dataList[27])))
        self.linechart.updateDisplay()
        # Update the basic information panel.
        dataList = (self.dataList[0], gv.DE_COMM, self.dataList[3],
                    self.dataList[4], self.dataList[9], self.dataList[27])
        self.infoPanel.updateData(dataList)
        # Update the multi-information panel Grid.
        self.multiInfoPg.updateSensorGrid(
            0, (self.dataList[0], self.dataList[4], self.dataList[27]))
        # Update the top view map panel.
        gv.iMapPanel.updatePPLNum(self.dataList[27])
        gv.iMapPanel.updateDisplay()

#--SensorReaderFrame-----------------------------------------------------------
    def OnClose(self, event):
        if not self.serComm is None:
            try:
                self.serComm.close()  # close the exists opened port.
            except:
                print("Error happend when close the serial port.")
            self.serComm = None 
        self.Destroy()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MyApp(wx.App):
    """ Init the frame and run the application"""
    def OnInit(self):
        mainFrame = SensorReaderFrame(None, -1, gv.APP_NAME)
        mainFrame.Show(True)
        return True

#-----------------------------------------------------------------------------
app = MyApp(0)
app.MainLoop()
