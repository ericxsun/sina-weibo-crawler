#encoding: utf-8

from common import STORE_PATH
from wx import html as wxhtml
from wx.lib import platebtn, wordwrap
import logo
import os
import re
import settings
import sina_weibo
import threading
import wx

HELP_DOC   = settings.LOCAL_CRAWLER_HELP_DOC 
HELP_TITLE = settings.LOCAL_CRAWLER_HELP_TITLE
WIN_STATUS = settings.LOCAL_CRAWLER_WIN_STATUS
WIN_TITLE  = settings.LOCAL_CRAWLER_WIN_TITLE

COPYRIGHT  = settings.COPYRIGHT
DEVELOPERS = settings.DEVELOPERS
HOME_PAGE  = settings.HOME_PAGE
LICENCE    = settings.LICENCE
VERSION    = settings.LOCAL_VERSION

DATA_CHOICES = settings.DATA_CHOICES

class StartCrawl(threading.Thread):
    def __init__(self, website, fetcher, fetch_data, ids, ids_type, 
                 store_path, window):
        threading.Thread.__init__(self)
        self.website    = website
        self.fetcher    = fetcher
        self.fetch_data = fetch_data
        self.ids        = ids
        self.ids_type   = ids_type
        self.store_path = store_path
        self.window     = window
        self._stop      = threading.Event()
        
        self.setDaemon(True)
        
    def run(self):
        #start the works
        if self.website == settings.SINA_WEIBO:
            if self.ids_type == 'uid':
                sina_weibo.main(fetcher=self.fetcher, uids=self.ids, 
                                fetch_data=self.fetch_data, 
                                store_path=self.store_path, window=self.window)
            elif self.ids_type == 'msg_url':
                sina_weibo.main(fetcher=self.fetcher, msg_urls=self.ids,
                                store_path=self.store_path, window=self.window)
        
        elif self.website == settings.TWITTER:
            msg = 'For twitter, not implemented in current version.'
            wx.CallAfter(self.window.write_logs, str(msg))
        elif self.website == settings.FACEBOOK:
            msg = 'For facebook, not implemented in current version.'
            wx.CallAfter(self.window.write_logs, str(msg))
        else:
            msg = 'For %s, not implemented in current version.' %self.website
            wx.CallAfter(self.window.write_logs, str(msg))
        
        #finished
        wx.CallAfter(self.window.finished)
    
    def stop(self):
        self._stop.set()

class SearchUserFrame(wx.Frame):
    def __init__(self):
        
        wx.Frame.__init__(self, parent=wx.GetApp().TopWindow, id=-1, 
                          title='Search Result', size=(500, 300),
                          style=wx.DEFAULT_FRAME_STYLE^(wx.MAXIMIZE_BOX|wx.RESIZE_BORDER))
        self.panel = wx.Panel(self)
        
        self.layout()
        
        self.Center()
                
    def layout(self):
        #
        self.SetIcon(logo.get_icon())
        
        #
        wx.StaticLine(parent=self.panel, id=-1, pos=(0, 0), size=(500, -1))
        wx.StaticText(parent=self.panel, id=-1, pos=(10, 5), size=(-1, -1),
                      label='To choose a user, please click the image.')
        self.search_res = wxhtml.HtmlWindow(parent=self.panel, id=-1, 
                                            pos=(10, 30), size=(480, 260),
                                            style=wxhtml.HW_SCROLLBAR_AUTO)
        self.search_res.SetPage('<b>Searching, please wait...</b>')
        
    def update(self, res):
        page = res
        self.search_res.SetPage(page)
        uid = 1 #to be the selected
        #return the selected user's id
        
        return uid
           
class TaskbarIco(wx.TaskBarIcon):
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.logo_ico = logo.get_icon()
        self.create_menu()
        
        #bind event
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.on_taskbar_leftdclick)
        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)
        
    def create_menu(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.on_popup)
        self.menu = wx.Menu()
        self.menu.Append(wx.ID_EXIT, 'Exit')
        
    def on_popup(self, event):
        self.PopupMenu(self.menu)
        
    def on_exit(self, event):
        msg = 'Are you sure to exist? Some data will lose.'
        ret = wx.MessageBox(message=msg, style=wx.OK | wx.CANCEL)
        
        if ret == wx.OK:
            self.RemoveIcon()
            self.frame.Destroy()
            self.Destroy()
            wx.GetApp().ExitMainLoop()
              
            os._exit(0)
        
    def on_taskbar_leftdclick(self, event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)

        if not self.frame.IsShown():
            self.frame.Show(True)
            
        self.frame.Raise()
                
    def set(self):
        self.SetIcon(self.logo_ico, 'Crawler System')
        
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
    def __init__(self, title, status, account_display=None, website_display=None, fetcher=None):
        wx.Frame.__init__(self, parent=None, id=-1, title=title, size=(565, 550),
                          style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.RESIZE_BOX))
        
        self.panel  = wx.Panel(self)
        self.tskbar = TaskbarIco(self)
        
        self.store_path      = STORE_PATH
        self.account_display = account_display
        self.website_display = website_display
        self.fetcher         = fetcher
        self.ids             = []
        self.single_flag     = True
                
        self.layout(status)
        self.Center()
        
        #bind event
        self.Bind(wx.EVT_CLOSE, self.on_taskbar)
        self.Bind(wx.EVT_BUTTON, self.on_help, self.help_btn)
        self.Bind(wx.EVT_BUTTON, self.on_path_setting, self.path_setting_btn)
        self.Bind(wx.EVT_BUTTON, self.on_single_user_id, self.single_user_id_btn)
        self.Bind(wx.EVT_BUTTON, self.on_multi_user_id, self.multi_user_id_btn)
        self.Bind(wx.EVT_BUTTON, self.on_msg_url, self.msg_url_btn)
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.on_search, self.single_user_id_search)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_search, self.single_user_id_search)
        self.Bind(wx.EVT_BUTTON, self.on_start, self.start_btn)
        
    def layout(self, status):
        self.SetIcon(logo.get_icon())
        
        self.SetBackgroundColour('MEDIA GRAY')
        wx.StaticLine(parent=self.panel, id=-1, pos=(0, 0), size=(600, -1), 
                      style=wx.ALL|wx.EXPAND)
        
        #Basic Infos: Account+WebSite+Help
        wx.StaticText(parent=self.panel, id=-1, 
                      label='Account:'+self.account_display,
                      pos=(25, 5), size=(285, 25), style=wx.TE_RICH2)
        wx.StaticText(parent=self.panel, id=-1, 
                      label='WebSite:'+self.website_display,
                      pos=(300, 5), size=(200, 25), style=wx.TE_RICH2)
        self.help_btn = platebtn.PlateButton(parent=self.panel, id_=-1, 
                                             label='Help?', pos=(490, 2), 
                                             size=(50, 25),
                                             style=platebtn.PB_STYLE_NOBG|
                                             platebtn.PB_STYLE_GRADIENT)
        
        #
        wx.StaticLine(parent=self.panel, id=-1, pos=(0, 30), size=(600, -1), 
                      style=wx.ALL|wx.EXPAND)
        
        #Path Setting
        self.path_setting_btn = wx.Button(parent=self.panel, id=-1, 
                                          pos=(20, 35), size=(120, 30), 
                                          label='Path Setting')
        self.path_setting_txt = wx.TextCtrl(parent=self.panel, id=-1, 
                                            value=self.store_path,
                                            pos=(142, 37), size=(398, 27),
                                            style=wx.TE_RICH2|wx.TE_READONLY)
        self.path_setting_txt.SetBackgroundColour(self.GetBackgroundColour())
        
        #
        wx.StaticLine(parent=self.panel, id=-1, pos=(0, 70), size=(600, -1), 
                      style=wx.ALL|wx.EXPAND)
        
        #Single User ID/Multi-User ID/message chain
        self.single_user_id_btn = wx.Button(parent=self.panel, id=-1, 
                                            label='Nick Name',
                                            pos=(20, 79), size=(120, 30))
        self.single_user_id_search = wx.SearchCtrl(parent=self.panel, id=-1, 
                                                   pos=(142, 79), size=(235, 28),
                                                   style=wx.TE_RICH2|wx.TE_PROCESS_ENTER)
        self.multi_user_id_btn = wx.Button(parent=self.panel, id=-1, 
                                           label='Multi User ID',
                                           pos=(20, 109), size=(120, 30))
        self.multi_user_id_txt = wx.TextCtrl(parent=self.panel, id=-1, value='',
                                             pos=(142, 79), size=(235, 90),
                                             style=wx.TE_RICH2|wx.TE_MULTILINE)
        self.msg_url_btn = wx.Button(parent=self.panel, id=-1, label='Message URL',
                                     pos=(20, 140), size=(120, 30))
        self.msg_url_txt = wx.TextCtrl(parent=self.panel, id=-1, value='', 
                                       pos=(142, 79), size=(235, 90), 
                                       style=wx.TE_RICH2|wx.TE_MULTILINE)
        
        self.multi_user_id_btn.Enable(False)
        self.single_user_id_btn.Enable(True)
        self.single_user_id_search.Show(False)
        self.msg_url_btn.Enable(True)
        self.msg_url_txt.Show(False)
        
        #Fetch Data Type
        self.fetch_data_type= wx.RadioBox(parent=self.panel, id=-1, 
                                          label='Fetch Data Type',
                                          pos=(390, 72), size=(150, 98),
                                          majorDimension=2,
                                          style=wx.RA_SPECIFY_COLS,
                                          choices=DATA_CHOICES)
        self.fetch_data_type.SetSelection(0)
        
        #
        wx.StaticLine(parent=self.panel, id=-1, pos=(0, 176), size=(600, -1), 
                      style=wx.ALL|wx.EXPAND)
        
        #Start
        self.start_btn = wx.Button(parent=self.panel, id=-1, label='Start',
                                   pos=(440, 185), size=(100, 40))
        
        #progress bar/ clear logs
        wx.RadioBox(parent=self.panel, id=-1, label='Progressing',
                    pos=(20, 180), size=(360, 55),
                    style=wx.RA_HORIZONTAL, choices=[''])
        self.progress_bar = wx.Gauge(parent=self.panel, id=-1, range=100, 
                                     pos=(25, 200), size=(350, 30),
                                     style=wx.GA_HORIZONTAL)
        self.progress_bar.SetValue(0)
                
        values  = 'Login succeed...\nCurrent User:' + self.account_display + '\n'
        values += 'Current WebSite:' + self.website_display +'\n'
        values += 'Current Version of Crawler:' + VERSION +'\n'
        self.logs_txt = wx.TextCtrl(parent=self.panel, id=-1, value=values,
                                    pos=(20, 260), size=(520, 250),
                                    style=wx.TE_READONLY|wx.TE_RICH2|wx.TE_MULTILINE)

        #status
        stbar = MyStatusBar(self)
        self.SetStatusBar(stbar)         
        
    def on_help(self, event):
        info = wx.AboutDialogInfo()
        info.SetIcon(logo.get_icon())
   
        info.Name        = 'Crawler Client'
        info.Version     = VERSION
        info.Copyright   = COPYRIGHT
        info.Description = wordwrap.wordwrap(text=HELP_DOC, width=350, 
                                             dc=wx.ClientDC(self.panel),
                                             breakLongWords=True, margin=0)
        info.WebSite    = (HOME_PAGE, 'Home Page')
        info.Developers = DEVELOPERS
        info.Licence    = LICENCE
        
        wx.AboutBox(info)
    
    def on_path_setting(self, event):
        dialog = wx.DirDialog(parent=None, message='Choose a directory', 
                              style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.store_path = dialog.GetPath()
            self.path_setting_txt.SetValue(self.store_path)
            
        dialog.Destroy()
    
    def on_single_user_id(self, event):
        self.single_user_id_btn.Enable(False)
        self.multi_user_id_btn.Enable(True)
        self.msg_url_btn.Enable(True)
        
        self.single_user_id_search.Show(True)
        self.multi_user_id_txt.Show(False)
        self.msg_url_txt.Show(False)
    
        self.fetch_data_type.Enable(True)
        
        self.single_flag = True
        
    def on_multi_user_id(self, event):
        self.single_user_id_btn.Enable(True)
        self.multi_user_id_btn.Enable(False)
        self.msg_url_btn.Enable(True)
        
        self.single_user_id_search.Show(False)
        self.multi_user_id_txt.Show(True)
        self.msg_url_txt.Show(False)
        
        self.fetch_data_type.Enable(True)
        
        self.single_flag = False
    
    def on_msg_url(self, event):
        self.single_user_id_btn.Enable(True)
        self.multi_user_id_btn.Enable(True)
        self.msg_url_btn.Enable(False)
        
        self.single_user_id_search.Show(False)
        self.multi_user_id_txt.Show(False)
        self.msg_url_txt.Show(True)
        
        self.fetch_data_type.Enable(False)
        
        self.single_flag = False        
    
    def on_search(self, event):
        query = (self.single_user_id_search.Value).strip()
        query = query.encode('UTF-8')
        
        wx.MessageBox(message='Not implemented.')
        return

        search_res = SearchUserFrame()
    
        if query != '':
            res = self.fetcher.search_user(query)
            
            search_res.Show(True)
             
            self.ids = search_res.update(res if res is not None else 'Not Find!')
        
    def on_start(self, event):
        self.progress_bar.SetValue(0)          
        self.ids = []
        id_type = 'uid'
        
        if not self.msg_url_btn.IsEnabled():
            id_type = 'msg_url'
            _ids = self.msg_url_txt.Value.split(';')
            _ids = [_id.strip().encode('UTF-8') for _id in _ids if len(_id) > 0]
            
            p = re.compile(r'^http[s]?://weibo.com/\d*/[A-Za-z0-9]+$', re.U)
            for _id in _ids:
                try:
                    if len(_id) > 0:
                        _id = p.search(_id).group(0)
                        self.ids.append(_id)
                except:
                    msg = ('Discard [%s] for not like:'
                           ' "http://weibo.com/1000000253/ezC36cq3i6G".' %str(_id))
                    self.write_logs(msg)
            
            if len(self.ids) == 0:
                wx.MessageBox(message='No Message URL, please retry.')
                self.msg_url_txt.SetValue('')
                return
        else:
            if not self.single_user_id_btn.IsEnabled():
                wx.MessageBox(message='Selected user in search result. At present, not implemented.')
                return
            elif not self.multi_user_id_btn.IsEnabled():
                _ids = self.multi_user_id_txt.Value.split(';')
                _ids = [_id.strip().encode('UTF-8') for _id in _ids if len(_id) > 0]
                
                for _id in _ids:
                    try:
                        if len(_id) > 0:
                            int(_id)
                            self.ids.append(_id)
                    except ValueError:
                        msg = ('Discard [%s] for containing other characters'
                               ' besides digital.' %str(_id))
                        self.write_logs(msg)
                        
                if len(self.ids) == 0:
                    wx.MessageBox(message='No User ID, please retry.')
                    self.multi_user_id_txt.SetValue('')
                    return

        fetch_data = DATA_CHOICES[self.fetch_data_type.GetSelection()]
        wbs = self.website_display
        fetcher = self.fetcher
        ids = self.ids
        crawler = StartCrawl(wbs, fetcher, fetch_data, ids, id_type, 
                             self.store_path, self)
        crawler.start()
        
        self.path_setting_btn.Enable(False)
        
        self.single_user_id_btn.Enable(False)
        self.multi_user_id_btn.Enable(False)
        self.msg_url_btn.Enable(False)
        
        self.fetch_data_type.Enable(False)
        
        self.start_btn.Enable(False)
        
    def finished(self):
        self.path_setting_btn.Enable(True)
        
        self.single_user_id_btn.Enable(True)
        self.multi_user_id_btn.Enable(False)
        self.msg_url_btn.Enable(True)
        
        self.fetch_data_type.Enable(True)
        
        self.start_btn.Enable(True)
    
    def on_clear_logs(self, event):
        self.logs_txt.SetValue('')
    
    def write_logs(self, log):
        rows = self.logs_txt.GetNumberOfLines()
    
        MAX_ROWS = 500
        if rows > MAX_ROWS:
            self.logs_txt.Clear()
        last_pos = self.logs_txt.GetLastPosition()
        self.logs_txt.SetInsertionPoint(last_pos)
        self.logs_txt.SetInsertionPoint(last_pos)
        self.logs_txt.WriteText(log + '\n')
    
    def on_close(self, event):
        ret = wx.MessageBox(message="Are you sure to exist?", style=wx.OK | wx.CANCEL)
        
        if ret == wx.OK:
            self.tskbar.RemoveIcon()
            self.tskbar.Destroy()
            self.Destroy()
            wx.GetApp().ExitMainLoop()
              
            os._exit(0)
            
    def on_taskbar(self, event):
        self.Show(False)
        self.tskbar.set()

    def update_progress_bar(self, count):
        self.progress_bar.SetValue(count)
        
    def verify_code(self, pic):
        raise NotImplementedError

class Window(wx.App):
    def __init__(self, account_display=None, website_display=None, fetcher=None):
        
        wx.App.__init__(self)
        self.frame = Frame(WIN_TITLE, WIN_STATUS, account_display, website_display, fetcher)
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        
def main(*args, **kwargs):
    win = Window(*args, **kwargs)
    win.MainLoop()