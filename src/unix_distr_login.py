#encoding: utf-8

from wx.lib import hyperlink
import logo
import settings
import wx

WIN_TITLE  = settings.DISTR_LOGIN_WIN_TITLE
WIN_STATUS = settings.DISTR_LOGIN_WIN_STATUS
HOME_PAGE  = settings.HOME_PAGE

class MyStatusBar(wx.StatusBar):
    '''
    my status bar for displaying the message in the bottom right corner.
    '''
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)
        self.SetFieldsCount(1)
        self.msg_label = wx.StaticText(parent=self, id=-1, label=WIN_STATUS)
        self.reposition_message()

        self.Bind(wx.EVT_SIZE, self.on_resize)

    def on_resize(self, event):
        self.reposition_message()

    def reposition_message(self):
        field_rect = self.GetFieldRect(0)
        label_rect = self.msg_label.GetRect()
        width_diff = field_rect.width - label_rect.width

        field_rect.width = label_rect.width
        field_rect.x += width_diff
        field_rect.y += 3

        self.msg_label.SetRect(field_rect)

class Frame(wx.Frame):
    def __init__(self, title, status):
        wx.Frame.__init__(self, parent=None, id=-1, title=title, 
                          size=(290, 180),
                          style=wx.DEFAULT_FRAME_STYLE^(wx.MAXIMIZE_BOX|wx.RESIZE_BORDER))
        
        self.panel = wx.Panel(self)       
        self.layout(status)  
        
        self.Center()
        self.Show(True)
        
        #bind event
        self.Bind(wx.EVT_BUTTON, self.on_login, self.login_btn)
                
    def layout(self, status):
        #widgets
                
        #logo
        self.SetIcon(logo.get_icon())
        
        wx.StaticLine(parent=self.panel, id=-1, pos=(0, 0), size=(300, -1), 
                      style=wx.ALL|wx.EXPAND)      
        
        #Account + Password      
        wx.StaticText(parent=self.panel, id=-1, label='Account:',
                      pos=(25, 19), size=(60, 30))
        self.account  = wx.TextCtrl(parent=self.panel, id=-1, value='',
                                    pos=(90, 15), size=(180, 30))
         
        wx.StaticText(parent=self.panel, id=-1, label='Password:',
                      pos=(20, 55), size=(65, 30))
        self.password = wx.TextCtrl(parent=self.panel, id=-1, value='',
                                    pos=(90, 50), size=(180, 30), 
                                    style=wx.TE_PASSWORD)
        
        #Login btn
        self.login_btn = wx.Button(parent=self.panel, id=-1, label='Login',
                                   pos=(125, 85), size=(90, 35))
        
        wx.StaticLine(parent=self.panel, id=-1, pos=(0, 125), size=(300, -1), 
                      style=wx.ALL|wx.EXPAND)
        
        #site link
        wx.StaticText(parent=self.panel, id=-1, label='Home Page:',
                      pos=(30, 135), size=(90, 30))
        self.link = hyperlink.HyperLinkCtrl(parent=self.panel, id=-1, pos=(115, 135))
        self.link.SetURL(URL=HOME_PAGE)
        self.link.SetLabel(label=HOME_PAGE)
        
        #status
        stbar = MyStatusBar(self)
        self.SetStatusBar(stbar)        
        
    def on_login(self, event):
        account = self.account.GetValue().strip()
        password= self.password.GetValue().strip()
        
        if (account is None or len(account) == 0 or 
            password is None or len(password) == 0):
            msg = 'Account/Password cannot be blank! Please retry!'
            wx.MessageBox(message=msg, caption='Warning', style=wx.OK|wx.ICON_INFORMATION)
        
        wx.MessageBox(message='Not Implemented')
              
class Window(wx.App):
    def __init__(self, title, status):
        wx.App.__init__(self)
        self.frame = Frame(title, status)
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        
def main(*args, **kwargs):
    Window(WIN_TITLE, WIN_STATUS).MainLoop()
    
if __name__ == '__main__':
    main()   
