#Boa:Frame:Frame1

import wx

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTONREAD, wxID_FRAME1BUTTONWRITE, 
 wxID_FRAME1PANEL1, wxID_FRAME1STATICBOX1, wxID_FRAME1STATICTEXT1, 
 wxID_FRAME1STATICTEXT2, wxID_FRAME1STATUSBAR1, wxID_FRAME1TEXTCTRL1, 
 wxID_FRAME1TEXTCTRLCYCLECONFIG, wxID_FRAME1TEXTCTRLINITCONFIG, 
] = [wx.NewId() for _init_ctrls in range(11)]

class Frame1(wx.Frame):
    def _init_coll_menuBar1_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.MenuSettings, title=u'File')

    def _init_utils(self):
        # generated method, don't edit
        self.menuBar1 = wx.MenuBar()

        self.MenuSettings = wx.Menu(title=u'Settings...')

        self._init_coll_menuBar1_Menus(self.menuBar1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(418, 306), size=wx.Size(509, 315),
              style=wx.DEFAULT_FRAME_STYLE, title='Switch Configurator')
        self._init_utils()
        self.SetClientSize(wx.Size(509, 287))
        self.SetMenuBar(self.menuBar1)

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME1STATUSBAR1,
              name='statusBar1', parent=self, style=0)
        self.SetStatusBar(self.statusBar1)

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(509, 265),
              style=wx.TAB_TRAVERSAL)

        self.staticBox1 = wx.StaticBox(id=wxID_FRAME1STATICBOX1,
              label=u'Configurations', name='staticBox1', parent=self.panel1,
              pos=wx.Point(16, 16), size=wx.Size(480, 104), style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL1, name='textCtrl1',
              parent=self.panel1, pos=wx.Point(16, 128), size=wx.Size(480, 128),
              style=wx.TE_READONLY | wx.TE_MULTILINE | wx.VSCROLL, value=u'')

        self.textCtrlInitConfig = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLINITCONFIG,
              name=u'textCtrlInitConfig', parent=self.panel1, pos=wx.Point(152,
              40), size=wx.Size(192, 27), style=0, value=u'{0, 11, 0, 0}')

        self.textCtrlCycleConfig = wx.TextCtrl(id=wxID_FRAME1TEXTCTRLCYCLECONFIG,
              name=u'textCtrlCycleConfig', parent=self.panel1, pos=wx.Point(152,
              80), size=wx.Size(192, 27), style=0, value=u'{1, 0, 0, 0}')

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'Init Config', name='staticText1', parent=self.panel1,
              pos=wx.Point(56, 48), size=wx.Size(73, 17), style=0)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=u'Cycle Config', name='staticText2', parent=self.panel1,
              pos=wx.Point(56, 88), size=wx.Size(85, 17), style=0)

        self.buttonRead = wx.Button(id=wxID_FRAME1BUTTONREAD, label=u'Read',
              name=u'buttonRead', parent=self.panel1, pos=wx.Point(384, 40),
              size=wx.Size(85, 29), style=0)
        self.buttonRead.Bind(wx.EVT_BUTTON, self.OnButtonReadButton,
              id=wxID_FRAME1BUTTONREAD)

        self.buttonWrite = wx.Button(id=wxID_FRAME1BUTTONWRITE, label=u'Write',
              name=u'buttonWrite', parent=self.panel1, pos=wx.Point(384, 80),
              size=wx.Size(85, 29), style=0)
        self.buttonWrite.Bind(wx.EVT_BUTTON, self.OnButtonWriteButton,
              id=wxID_FRAME1BUTTONWRITE)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButtonReadButton(self, event):
        event.Skip()

    def OnButtonWriteButton(self, event):
        event.Skip()


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show()

    app.MainLoop()
