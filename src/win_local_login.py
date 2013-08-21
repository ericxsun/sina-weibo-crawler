#encoding: utf-8

from sina_weibo.fetcher import ComWeiboFetcher
from wx.lib import hyperlink
import logo
import settings
import wx

HOME_PAGE    = settings.HOME_PAGE
SITE_CHOICES = settings.SITE_CHOICES
WIN_STATUS   = settings.LOCAL_LOGIN_WIN_STATUS
WIN_TITLE    = settings.LOCAL_LOGIN_WIN_TITLE

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
    def __init__(self, title=None, status=None):
        if title is None:
            title = ''
            
        wx.Frame.__init__(self, parent=None, id=-1, title=title, 
                          size=(305, 230),
                          style=wx.DEFAULT_FRAME_STYLE^(wx.MAXIMIZE_BOX|wx.RESIZE_BORDER))
        
        self.panel = wx.Panel(self)       
        self.layout(status)  
        
        self.Center()
        self.Show(True)
        
        #bind event
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_BUTTON, self.on_login, self.login_btn)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_login, self.password)
        
    def layout(self, status):
        #logo
        self.SetIcon(logo.get_icon())
        
        #
        wx.StaticLine(parent=self.panel, id=-1, pos=(0, 0), size=(300, -1), 
                      style=wx.ALL|wx.EXPAND)
                
        #WebSite + Account + Password
        wx.StaticText(parent=self.panel, id=-1, label=u'WebSite:', 
                      pos=(24, 15), size=(60, 30))
        self.website  = wx.Choice(parent=self.panel, id=-1,
                                  pos=(90, 7), size=(180, 30),
                                  choices=SITE_CHOICES)
        self.website.SetSelection(0)
        
        wx.StaticText(parent=self.panel, id=-1, label=u'Account:',
                      pos=(25, 47), size=(60, 30))
        self.account  = wx.TextCtrl(parent=self.panel, id=-1, value='',
                                    pos=(90, 42), size=(180, 30))
         
        wx.StaticText(parent=self.panel, id=-1, label=u'Password:',
                      pos=(20, 85), size=(65, 30))
        self.password = wx.TextCtrl(parent=self.panel, id=-1, value='',
                                    pos=(90, 77), size=(180, 30), 
                                    style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        
        #Login btn
        self.login_btn = wx.Button(parent=self.panel, id=-1, label=u'Login',
                                   pos=(125, 110), size=(90, 35))
        
        #
        wx.StaticLine(parent=self.panel, id=-1, pos=(0, 147), size=(300, -1), 
                      style=wx.ALL|wx.EXPAND)
        
        #site link
        wx.StaticText(parent=self.panel, id=-1, label=u'Home Page:',
                      pos=(30, 155), size=(90, 30))
        self.link = hyperlink.HyperLinkCtrl(parent=self.panel, id=-1, pos=(115, 155))
        self.link.SetURL(URL=HOME_PAGE)
        self.link.SetLabel(label=HOME_PAGE)
        self.link.SetBackgroundColour(self.GetBackgroundColour())
        
        #status
        stbar = MyStatusBar(self)
        self.SetStatusBar(stbar)        

    def on_login(self, event):
        website = SITE_CHOICES[self.website.GetCurrentSelection()]
        account = self.account.GetValue().strip().encode('UTF-8')
        password= self.password.GetValue().strip().encode('UTF-8')
        
        if (account is None or len(account) == 0 or 
            password is None or len(password) == 0):
            wx.MessageBox(message='Account/Password cannot be blank. Please retry!',
                          caption='Warning', style=wx.OK|wx.ICON_INFORMATION)
        else:
            if website == settings.SINA_WEIBO:         
                fetcher = ComWeiboFetcher(username=account, password=password, 
                                          window=self)
                if fetcher.check_cookie():
                    fetcher.window = None
                    
                    self.Destroy()
                    wx.GetApp().ExitMainLoop()
                    
                    import win_local_crawler as wlc
                    wlc.main(account_display=account, website_display=website,
                             fetcher=fetcher)
            elif website == settings.TWITTER:
                wx.MessageBox(message='For Twitter: not implemented. Please retry!',
                              caption='Error', style=wx.OK|wx.ICON_INFORMATION)
            elif website == settings.FACEBOOK:
                wx.MessageBox(message='For Facebook: not implemented. Please retry!',
                              caption='Error', style=wx.OK|wx.ICON_INFORMATION)
    
    def on_close(self, event):
        wx.GetApp().ExitMainLoop()
                               
    def show_msg(self, msg):
        wx.MessageBox(message=msg)

class Window(wx.App):
    def __init__(self, title=None, status=None):
        wx.App.__init__(self)
        self.frame = Frame(title=title, status=status)
        self.SetTopWindow(self.frame)
        self.frame.Show(True)

def main(*args, **kwargs):
    Window(status=WIN_STATUS).MainLoop()
    
if __name__ == '__main__':
    main()