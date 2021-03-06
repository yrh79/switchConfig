#Boa:Frame:Frame1

import wx
import wx.lib.newevent
import threading
import serial
import serial.tools.list_ports as lp

# ----------------------------------------------------------------------
# Create an own event type, so that GUI updates can be delegated
# this is required as on some platforms only the main thread can
# access the GUI without crashing. wxMutexGuiEnter/wxMutexGuiLeave
# could be used too, but an event is more elegant.

(SerialRxEvent, EVT_SERIALRX) = wx.lib.newevent.NewEvent()

# ----------------------------------------------------------------------
# Serial handling thread:
# It would exit automatically if the port is not connected with an
# Auto Switch device.

class mySerialThread(threading.Thread):

    def __init__(self, ownerFrame, portName, old_wx=False):
        threading.Thread.__init__(self)
        self.ownerFrame = ownerFrame
        self.portName = portName
        self.serial = None
        self.alive = threading.Event()
        self.rxBuf = bytearray()
        self.timer = wx.CallLater(10*1000, self.stop)
        self.setDaemon(1)
        self.confirmed = False
        self.old_wx = old_wx

    def stop(self):
        self.alive.clear()

    def run(self):
        self.alive.set()
        #print "trying {} ...".format(self.portName)
        try:
            self.serial = serial.Serial(self.portName, 115200, timeout=1)  # open serial port
        except:
            return

        while self.alive.isSet():
            s = None
            try:
                if self.old_wx:
                    s = self.serial.read(1)
                else:
                    s = self.serial.read(self.serial.in_waiting or 1)
            except:
                return

            if s:
                if self.confirmed:
                    self.ownerFrame.NotifySerialRx(s)
                else:
                    for b in s:
                        self.rxBuf.append(b)

                        if b == '\n':
                            msg = self.rxBuf.decode()
                            if "Auto Switch initialized..." in msg:
                                self.timer.Stop()
                                self.confirmed = True
                                self.ownerFrame.NotifySerialSelected(self.portName, self.serial)
                                del self.timer

                            self.rxBuf = bytearray()


# ----------------------------------------------------------------------


def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTONREAD, wxID_FRAME1BUTTONWRITE, 
 wxID_FRAME1PANEL1, wxID_FRAME1STATICBOX1, wxID_FRAME1STATICBOX2, 
 wxID_FRAME1STATICBOX3, wxID_FRAME1STATICBOX4, wxID_FRAME1STATICBOX5, 
 wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT2, wxID_FRAME1STATUSBAR1, 
 wxID_FRAME1TEXTCTRLCYCLECONFIG_DAY, wxID_FRAME1TEXTCTRLCYCLECONFIG_HOUR, 
 wxID_FRAME1TEXTCTRLCYCLECONFIG_MIN, wxID_FRAME1TEXTCTRLCYCLECONFIG_SEC, 
 wxID_FRAME1TEXTCTRLINITCONFIG_DAY, wxID_FRAME1TEXTCTRLINITCONFIG_HOUR, 
 wxID_FRAME1TEXTCTRLINITCONFIG_MIN, wxID_FRAME1TEXTCTRLINITCONFIG_SEC, 
 wxID_FRAME1TEXTCTRLOUTPUT, 
] = [wx.NewId() for _init_ctrls in range(21)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(418, 334), size=wx.Size(508, 363),
              style=wx.DEFAULT_FRAME_STYLE, title='Switch Configurator')
        self.SetClientSize(wx.Size(508, 335))

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME1STATUSBAR1,
              name='statusBar1', parent=self, style=0)
        self.SetStatusBar(self.statusBar1)

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(508, 313),
              style=wx.TAB_TRAVERSAL)

        self.staticBox1 = wx.StaticBox(id=wxID_FRAME1STATICBOX1,
              label=u'Configurations', name='staticBox1', parent=self.panel1,
              pos=wx.Point(16, 8), size=wx.Size(480, 136), style=0)

        self.textCtrlOutput = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLOUTPUT,
              name='textCtrlOutput', parent=self.panel1, pos=wx.Point(16, 152),
              size=wx.Size(480, 152),
              style=wx.TE_READONLY | wx.TE_MULTILINE | wx.VSCROLL, value=u'')

        self.textCtrlInitConfig_day = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLINITCONFIG_DAY,
              name=u'textCtrlInitConfig_day', parent=self.panel1,
              pos=wx.Point(136, 56), size=wx.Size(40, 27), style=0, value=u'')

        self.textCtrlCycleConfig_day = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLCYCLECONFIG_DAY,
              name=u'textCtrlCycleConfig_day', parent=self.panel1,
              pos=wx.Point(136, 96), size=wx.Size(40, 27), style=0, value=u'')

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'Init Config', name='staticText1', parent=self.panel1,
              pos=wx.Point(32, 64), size=wx.Size(73, 17), style=0)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=u'Cycle Config', name='staticText2', parent=self.panel1,
              pos=wx.Point(24, 104), size=wx.Size(85, 17), style=0)

        self.buttonRead = wx.Button(id=wxID_FRAME1BUTTONREAD, label=u'Read',
              name=u'buttonRead', parent=self.panel1, pos=wx.Point(384, 56),
              size=wx.Size(85, 29), style=0)
        self.buttonRead.Bind(wx.EVT_BUTTON, self.OnButtonReadButton,
              id=wxID_FRAME1BUTTONREAD)

        self.buttonWrite = wx.Button(id=wxID_FRAME1BUTTONWRITE, label=u'Write',
              name=u'buttonWrite', parent=self.panel1, pos=wx.Point(384, 96),
              size=wx.Size(85, 29), style=0)
        self.buttonWrite.Bind(wx.EVT_BUTTON, self.OnButtonWriteButton,
              id=wxID_FRAME1BUTTONWRITE)

        self.textCtrlInitConfig_hour = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLINITCONFIG_HOUR,
              name=u'textCtrlInitConfig_hour', parent=self.panel1,
              pos=wx.Point(200, 56), size=wx.Size(40, 27), style=0, value=u'')

        self.textCtrlCycleConfig_hour = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLCYCLECONFIG_HOUR,
              name=u'textCtrlCycleConfig_hour', parent=self.panel1,
              pos=wx.Point(200, 96), size=wx.Size(40, 27), style=0, value=u'')

        self.textCtrlInitConfig_min = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLINITCONFIG_MIN,
              name=u'textCtrlInitConfig_min', parent=self.panel1,
              pos=wx.Point(264, 56), size=wx.Size(40, 27), style=0, value=u'')

        self.textCtrlCycleConfig_min = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLCYCLECONFIG_MIN,
              name=u'textCtrlCycleConfig_min', parent=self.panel1,
              pos=wx.Point(264, 96), size=wx.Size(40, 27), style=0, value=u'')

        self.textCtrlInitConfig_sec = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLINITCONFIG_SEC,
              name=u'textCtrlInitConfig_sec', parent=self.panel1,
              pos=wx.Point(328, 56), size=wx.Size(40, 27), style=0, value=u'')

        self.textCtrlCycleConfig_sec = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLCYCLECONFIG_SEC,
              name=u'textCtrlCycleConfig_sec', parent=self.panel1,
              pos=wx.Point(328, 96), size=wx.Size(40, 27), style=0, value=u'')

        self.staticBox2 = wx.StaticBox(id=wxID_FRAME1STATICBOX2, label=u'Hour',
              name='staticBox2', parent=self.panel1, pos=wx.Point(192, 32),
              size=wx.Size(56, 100), style=0)

        self.staticBox3 = wx.StaticBox(id=wxID_FRAME1STATICBOX3, label=u'Day',
              name='staticBox3', parent=self.panel1, pos=wx.Point(128, 32),
              size=wx.Size(56, 100), style=0)

        self.staticBox4 = wx.StaticBox(id=wxID_FRAME1STATICBOX4, label=u'Min',
              name='staticBox4', parent=self.panel1, pos=wx.Point(256, 32),
              size=wx.Size(56, 100), style=0)

        self.staticBox5 = wx.StaticBox(id=wxID_FRAME1STATICBOX5, label=u'Sec',
              name='staticBox5', parent=self.panel1, pos=wx.Point(320, 32),
              size=wx.Size(56, 100), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)

        ## threading
        self.threads = []
        self.serial = None
        self.Bind(EVT_SERIALRX, self.OnSerialRead)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.rxBuf = bytearray()
        self.connected = threading.Event()

    def OnButtonReadButton(self, event):
        self.serial.write(b'$get\r\n')

    def OnButtonWriteButton(self, event):
        if self.connected.isSet():
            i_d = self.textCtrlInitConfig_day.GetValue().encode()
            i_h = self.textCtrlInitConfig_hour.GetValue().encode()
            i_m = self.textCtrlInitConfig_min.GetValue().encode()
            i_s = self.textCtrlInitConfig_sec.GetValue().encode()

            c_d = self.textCtrlCycleConfig_day.GetValue().encode()
            c_h = self.textCtrlCycleConfig_hour.GetValue().encode()
            c_m = self.textCtrlCycleConfig_min.GetValue().encode()
            c_s = self.textCtrlCycleConfig_sec.GetValue().encode()

            i = b'$init {'+i_d+", "+i_h+", "+i_m+", "+i_s+b'}\r\n'
            c = b'$cycle {'+c_d+", "+c_h+", "+c_m+", "+c_s+b'}\r\n'
            self.serial.write(i)
            self.serial.write(c)


    def OnClose(self, event):
        """Called on application shutdown."""
        for t in self.threads:
            if t.isAlive():
                t.stop()
                if t.serial is not None:
                    t.serial.close()
                t.join()

        self.Destroy()                  # close windows, exit app

#-------------------------------------- COM port handling --------------

    def startSerial(self):   
        for port in lp.comports():
            t = None
            try:
               t = mySerialThread(self, port.device)
            except AttributeError:
               t = mySerialThread(self, port[0], old_wx = True)
            t.start()
            self.threads.append(t)

    def WriteText(self, text):
        self.textCtrlOutput.AppendText(text)

    def OnSerialRead(self, event):
        """Handle input from the serial port."""
        s = event.value
        for b in s:
            self.rxBuf.append(b)
            if b == '\n':
                msg = self.rxBuf.decode()

                if "Init config:" in msg:
                    l = [x.strip(" ") \
                          for x in msg[13:].strip("{}\r\n").split(",")]
                    self.textCtrlInitConfig_day.Replace(0,-1, l[0])
                    self.textCtrlInitConfig_hour.Replace(0,-1, l[1])
                    self.textCtrlInitConfig_min.Replace(0,-1, l[2])
                    self.textCtrlInitConfig_sec.Replace(0,-1, l[3])

                if "Cycle config:" in msg:
                    l = [x.strip(" ") \
                          for x in msg[14:].strip("{}\r\n").split(",")]
                    self.textCtrlCycleConfig_day.Replace(0, -1, l[0])
                    self.textCtrlCycleConfig_hour.Replace(0, -1, l[1])
                    self.textCtrlCycleConfig_min.Replace(0, -1, l[2])
                    self.textCtrlCycleConfig_sec.Replace(0, -1, l[3])

                self.rxBuf = bytearray()

        self.WriteText(s.decode('UTF-8', 'replace'))

    def NotifySerialSelected(self, portName, serialPort):
        self.serial = serialPort
        self.statusBar1.SetStatusText("Connected to an Auto Switch on Serial Port: {}".format(portName))
        self.connected.set()
        self.serial.write(b'$get\r\n')

    def NotifySerialRx(self, data):
        event = SerialRxEvent(value=data)
        wx.PostEvent(self, event)

#-------------------------------------- COM port handling ends --------------

if __name__ == '__main__':
    app = wx.App()
    frame = create(None)
    frame.Show()
    frame.startSerial()

    app.MainLoop()
