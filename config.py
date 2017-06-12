
import wx

class ConfigFrame(wx.Frame):
    
    positions = ("Flat", "Inverted", "Straight Up", "Straight Down", "Knife Edge")
    rotations = ("Aileron", "Elevator", "Yaw")
    
    def __init__(self, config):
        super(ConfigFrame, self).__init__(parent=None, title="Configurartion", size=(250, 150))
        self.InitUI()
        self.config = config
    
    def InitUI(self):
        self.posButtons = [wx.ToggleButton(self, wx.ID_ANY, pos) for pos in self.positions]
        self.rotButtons = [wx.ToggleButton(self, wx.ID_ANY, rot) for rot in self.rotations]
        
        self.button_start = wx.Button(self, wx.ID_ANY, "START Training")
        
        self.Bind(wx.EVT_BUTTON, self.onStart, self.button_start)
        
        self.SetTitle("Configuration")
        self.SetBackgroundColour(wx.Colour(250, 250, 250))
        # self.button_start.SetBackgroundColour(wx.Colour(0, 170, 0))
        self.button_start.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_buttonrow2 = wx.BoxSizer(wx.VERTICAL)
        sizer_buttonRow1 = wx.BoxSizer(wx.VERTICAL)
        label_config = wx.StaticText(self, wx.ID_ANY, ("RC Control Trainer\nConfiguration"), style=wx.ALIGN_CENTER | wx.TE_MULTILINE)
        label_config.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        sizer_main.Add(label_config, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 7)
        
        for posButton in self.posButtons:
            sizer_buttonRow1.Add(posButton, 0, wx.EXPAND, 0)
        
        sizer_buttons.Add(sizer_buttonRow1, 1, wx.EXPAND, 0)
        
        for rotButton in self.rotButtons:
            sizer_buttonrow2.Add(rotButton, 0, wx.EXPAND, 0)
        
        sizer_buttons.Add(sizer_buttonrow2, 1, wx.EXPAND, 0)
        sizer_main.Add(sizer_buttons, 1, wx.ALL | wx.EXPAND, 5)
        sizer_main.Add(self.button_start, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        self.Layout()
        
        self.Centre()
        self.Show(True)
        
    def onStart(self, event):
        gotAPos = False
        gotARot = False
        for idx, position in zip(range(len(self.positions)), self.positions):
            value = self.posButtons[idx].GetValue()
            gotAPos |= value
            self.config.__setattr__(position.replace(" ",""), value)
        for idx, rotation in zip(range(len(self.rotations)), self.rotations):
            value = self.rotButtons[idx].GetValue()
            gotARot |= value
            self.config.__setattr__(rotation.replace(" ",""), value)
            
        if not gotAPos or not gotARot:
            wx.MessageBox("You need to select at least one options from the first column and one option from the second column", "Configuration Issue", wx.OK | wx.ICON_HAND)
            event.Skip()
        else:    
            self.Close()


class Config(object):
    
    def showDialog(self):
        ex = wx.App()
        ConfigFrame(self)
        ex.MainLoop()
        
        