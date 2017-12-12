#Boa:Frame:Frame1

import wx
import threading

# ----------------------------------------------------------------------
# Create an own event type, so that GUI updates can be delegated
# this is required as on some platforms only the main thread can
# access the GUI without crashing. wxMutexGuiEnter/wxMutexGuiLeave
# could be used too, but an event is more elegant.

SERIALRX = wx.NewEventType()
# bind to serial data receive events
EVT_SERIALRX = wx.PyEventBinder(SERIALRX, 0)

class SerialRxEvent(wx.PyCommandEvent):
    eventType = SERIALRX

    def __init__(self, windowID, data):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)
        
# ----------------------------------------------------------------------


def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTONREAD, wxID_FRAME1BUTTONWRITE, 
 wxID_FRAME1PANEL1, wxID_FRAME1STATICBOX1, wxID_FRAME1STATICTEXT1, 
 wxID_FRAME1STATICTEXT2, wxID_FRAME1STATUSBAR1, 
 wxID_FRAME1TEXTCTRLCYCLECONFIG, wxID_FRAME1TEXTCTRLINITCONFIG, 
 wxID_FRAME1TEXTCTRLOUTPUT, 
] = [wx.NewId() for _init_ctrls in range(11)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(418, 306), size=wx.Size(516, 328),
              style=wx.DEFAULT_FRAME_STYLE, title='Switch Configurator')
        self.SetClientSize(wx.Size(508, 301))

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME1STATUSBAR1,
              name='statusBar1', parent=self, style=0)
        self.SetStatusBar(self.statusBar1)

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(508, 281),
              style=wx.TAB_TRAVERSAL)

        self.staticBox1 = wx.StaticBox(id=wxID_FRAME1STATICBOX1,
              label=u'Configurations', name='staticBox1', parent=self.panel1,
              pos=wx.Point(16, 8), size=wx.Size(480, 96), style=0)

        self.textCtrlOutput = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLOUTPUT,
              name='textCtrlOutput', parent=self.panel1, pos=wx.Point(16, 120),
              size=wx.Size(480, 152),
              style=wx.TE_READONLY | wx.TE_MULTILINE | wx.VSCROLL, value=u'')

        self.textCtrlInitConfig = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLINITCONFIG,
              name=u'textCtrlInitConfig', parent=self.panel1, pos=wx.Point(152,
              24), size=wx.Size(192, 27), style=0, value=u'{0, 11, 0, 0}')

        self.textCtrlCycleConfig = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLCYCLECONFIG,
              name=u'textCtrlCycleConfig', parent=self.panel1, pos=wx.Point(152,
              64), size=wx.Size(192, 27), style=0, value=u'{1, 0, 0, 0}')

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'Init Config', name='staticText1', parent=self.panel1,
              pos=wx.Point(56, 32), size=wx.Size(73, 17), style=0)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=u'Cycle Config', name='staticText2', parent=self.panel1,
              pos=wx.Point(56, 72), size=wx.Size(85, 17), style=0)

        self.buttonRead = wx.Button(id=wxID_FRAME1BUTTONREAD, label=u'Read',
              name=u'buttonRead', parent=self.panel1, pos=wx.Point(384, 24),
              size=wx.Size(85, 29), style=0)
        self.buttonRead.Bind(wx.EVT_BUTTON, self.OnButtonReadButton,
              id=wxID_FRAME1BUTTONREAD)

        self.buttonWrite = wx.Button(id=wxID_FRAME1BUTTONWRITE, label=u'Write',
              name=u'buttonWrite', parent=self.panel1, pos=wx.Point(384, 64),
              size=wx.Size(85, 29), style=0)
        self.buttonWrite.Bind(wx.EVT_BUTTON, self.OnButtonWriteButton,
              id=wxID_FRAME1BUTTONWRITE)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        ## buffer to hold the incoming chars for further matching
        self.rxBuf = bytearray() 
        
        ## threading
        self.thread = None
        self.serial = None
        self.Bind(EVT_SERIALRX, self.OnSerialRead)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.alive = threading.Event()

    def OnButtonReadButton(self, event):
        self.serial.write(b'$get\r\n')

    def OnButtonWriteButton(self, event):
        if self.alive.isSet():
            self.serial.write(b'$init '+self.textCtrlInitConfig.GetValue().encode()+b'\r\n')
            self.serial.write(b'$cycle '+self.textCtrlCycleConfig.GetValue().encode()+b'\r\n')

    def StartThread(self):
        """Start the receiver thread"""
        self.thread = threading.Thread(target=self.ComPortThread)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()

    def OnClose(self, event):
        """Called on application shutdown."""
        self.StopThread()               # stop reader thread
        if self.serial is not None:
            self.serial.close()             # cleanup
        self.Destroy()                  # close windows, exit app
        
#-------------------------------------- COM port threading --------------   
    def startSerial(self):
        import serial
        if not self.alive.isSet():
            try:
                self.serial = ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # open serial port
                #print(ser.name)         # check which port was really used
                self.SetTitle("Auto Switch on Serial Port: {}".format(self.serial.name))
                self.StartThread()
                self.statusBar1.SetStatusText("Connected to an Auto Switch on Serial Port: {}".format(self.serial.name))
            except:
                self.statusBar1.SetStatusText("No active Auto Switch found!")
            
    def StopThread(self):
        """Stop the receiver thread, wait until it's finished."""
        if self.thread is not None:
            self.alive.clear()          # clear alive event for thread
            self.thread.join()          # wait until thread has finished
            self.thread = None
            
    def WriteText(self, text):
        self.textCtrlOutput.AppendText(text)
    
    def OnSerialRead(self, event):
        """Handle input from the serial port."""
        s = event.data
        for b in s:
            msg = self.rxBuf.decode()
            self.rxBuf.append(b)
            if b == '\n':
                if "Auto Switch initialized..." in msg:
                    self.serial.write(b'$get\r\n')
                    
                if "Init config:" in msg:
                    self.textCtrlInitConfig.Replace(0,-1, msg[13:])
                    
                if "Cycle config:" in msg:
                    self.textCtrlCycleConfig.Replace(0, -1, msg[14:])
                
                
                self.rxBuf = bytearray()
                    
        self.WriteText(s.decode('UTF-8', 'replace'))
        
    def ComPortThread(self):
        """\
        Thread that handles the incoming traffic. Does the basic input
        transformation (newlines) and generates an SerialRxEvent
        """
        while self.alive.isSet():
            b = self.serial.read(self.serial.in_waiting or 1)
            if b:
                event = SerialRxEvent(self.GetId(), b)
                self.GetEventHandler().AddPendingEvent(event)

#-------------------------------------- COM port threading ends --------------        
                
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show()
    frame.startSerial()

    app.MainLoop()
