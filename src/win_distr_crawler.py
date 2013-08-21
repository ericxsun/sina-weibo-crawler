# encoding: utf-8

from common import STORE_PATH, TASK_PATH, logger
from sina_weibo.fetcher import ComWeiboFetcher
from wx.lib import platebtn, wordwrap
import codecs
import logo
import os
import re
import settings
import sina_weibo
import tarfile
import threading
import wx

HELP_DOC   = settings.DISTR_CRAWLER_HELP_DOC 
HELP_TITLE = settings.DISTR_CRAWLER_HELP_TITLE
WIN_STATUS = settings.DISTR_CRAWLER_WIN_STATUS
WIN_TITLE  = settings.DISTR_CRAWLER_WIN_TITLE

COPYRIGHT  = settings.COPYRIGHT
DEVELOPERS = settings.DEVELOPERS
HOME_PAGE  = settings.HOME_PAGE
LICENCE    = settings.LICENCE
VERSION    = settings.DISTR_VERSION

SITE_CHOICES = settings.SITE_CHOICES

class StartCrawl(threading.Thread):
    def __init__(self, host_fetcher, website, fetcher, store_path, window):
        threading.Thread.__init__(self)

        self.host_fetcher = host_fetcher
                
        self.website    = website
        self.fetcher    = fetcher
        self.store_path = store_path
        
        self.upload_path = os.path.join(self.store_path, 'uploaded')
        
        if not os.path.exists(self.upload_path):
            os.makedirs(self.upload_path) 
        
        self.window = window
        
        self._stop = threading.Event()
        self.setDaemon(True)

    def run(self):
        while True:
            msg = '---Connect to the task manager for task allocation---'
            logger.info(msg)
            wx.CallAfter(self.window.write_logs, msg)
            
            
            task_id = self.request_task()
            if task_id is None:
                msg = '---No task exists---'
                logger.info(msg)
                wx.CallAfter(self.window.write_logs, msg)
                
                break
            
            msg = '---Start task: %s---' %task_id
            logger.info(msg)
            wx.CallAfter(self.window.write_logs, msg)
            
            tar_file = self.do_task()
            
            msg = '---Finish task: %s---' %task_id
            logger.info(msg)
            wx.CallAfter(self.window.write_logs, msg)
            
            msg = '---Upload: %s-%s---' %(task_id, tar_file)
            logger.info(msg)
            wx.CallAfter(self.window.write_logs, msg)
            
            self.upload_task(tar_file)
            
        #finished
        wx.CallAfter(self.window.finished)
    
    def request_task(self):
        '''task file format:
            task_id:**(time format) time.strftime('%Y-%m-%d-%H-%M', time.localtime())
            id_type:**(uid/msg_url)
            fetch_data: weibos/follows/fans/infos
            uids:(separated by semicolon)
            msg_urls:(separated by semicolon)
        '''
        
        return self.host_fetcher.request_task()
    
    def do_task(self):
        '''task file format:
            task_id:**(time format) time.strftime('%Y-%m-%d-%H-%M', time.localtime())
            id_type:**(uid/msg_url)
            fetch_data: weibos/follows/fans/infos
            uids:(separated by semicolon)
            msg_urls:(separated by semicolon)
        '''
        
        task_id    = ''
        id_type    = 'uid'
        fetch_data = 'infos'
        uids       = []
        msg_urls   = []
        
        tar_file = None
            
        f_task = os.path.join(TASK_PATH, 'task.dat')
        if os.path.exists(f_task):
            fp = codecs.open(f_task, 'r', 'utf-8')
                
            data = fp.readlines()
                
            #parse
            for line in data:
                line = line.strip()
                    
                if line.startswith('task_id:'):
                    task_id = line.split('task_id:')[-1]
                elif line.startswith('id_type:'):
                    id_type = line.split('id_type:')[-1]
                elif line.startswith('fetch_data:'):
                    fetch_data = line.split('fetch_data:')[-1]
                    fetch_data = fetch_data.lower()
                elif line.startswith('uids:'):
                    _uids = line.split('uids:')[-1]
                    _uids = _uids.split(';')
                    _uids = [uid.strip().encode('utf-8') for uid in _uids if len(uid) > 0]
                        
                    for uid in uids:
                        try:
                            int(uid)
                            uids.append(uid)
                        except:
                            pass
                        
                elif line.startswith('msg_urls:'):
                    _msg_urls = line.split('msg_urls:')[-1]
                    _msg_urls = _msg_urls.split(';')
                        
                    p = re.compile(r'^http[s]?://weibo.com/\d*/[A-Za-z0-9]+$', re.U)
                    for msg_url in _msg_urls:
                        try:
                            msg_url = p.search(msg_url).group(0)
                            msg_urls.append(msg_url)
                        except:
                            pass
                else:
                    msg = 'Task format error.'
                    logger.info(msg)
                    wx.CallAfter(self.window.write_logs, msg)
                    
                
            #start
            if id_type == 'uid' and len(uids) > 0:
                sina_weibo.main(fetcher=self.fetcher, fetch_data=fetch_data,
                                uids=uids, store_path=self.store_path, 
                                window=self.window)
                    
                files = os.listdir(self.store_path)
                files = filter(lambda f: fetch_data in f and f.endswith('.csv'), files)
            elif id_type == 'msg_url' and len(msg_urls) > 0:
                sina_weibo.main(fetcher=self.fetcher, msg_urls=msg_urls,
                                store_path=self.store_path, window=self.window)
                    
                files = os.listdir(self.store_path)
                files = filter(lambda f: 'reposts' in f or 'comments' in f and f.endswith('.csv'), files)
                    
            #compress and upload
            if len(files) > 0:
                tar_f = str(self.host_fetcher.username) + str(task_id) + '.tar.gz'
                tar_f = os.path.join(self.store_path, tar_f)
                    
                tar_file = tarfile.open(tar_f, 'w:bz2')
                tar_file.add(f_task, arcname='task.dat')
                    
                for f in files:
                    f_name = os.path.join(self.store_path, f)
                    tar_file.add(f_name, arcname=f)
                        
                    os.rename(f_name, os.path.join(self.upload_path, f)) 
                        
                tar_file.close()
                    
            os.remove(os.path.join(self.store_path, f_task))
            
        return tar_file
    
    def upload_task(self, tar_file):
        if tar_file is not None:
            upload_flag = self.host_fetcher.upload_task(tar_file)
            
            if upload_flag is True:
                msg = 'upload file succeeded'
            else:
                msg = 'upload file failed'
                
            logger.info(msg)
            wx.CallAfter(self.window.write_logs, msg)
    
    def stop(self):
        self._stop.set()

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
    def __init__(self, title, status, host_fetcher):
        wx.Frame.__init__(self, parent=None, id=-1, title=title, size=(565, 550),
                          style=wx.DEFAULT_FRAME_STYLE^(wx.MAXIMIZE_BOX|wx.RESIZE_BORDER))
        
        self.panel  = wx.Panel(self)
        self.tskbar = TaskbarIco(self)
        
        self.store_path   = STORE_PATH
        self.host_fetcher = host_fetcher
                
        self.layout(status)
        self.Center()
        
        #bind event
        self.Bind(wx.EVT_CLOSE, self.on_taskbar)
        self.Bind(wx.EVT_BUTTON, self.on_help, self.help_btn)
        self.Bind(wx.EVT_BUTTON, self.on_path_setting, self.path_setting_btn)
        self.Bind(wx.EVT_BUTTON, self.on_start, self.start_btn)
        
    def layout(self, status):
        self.SetIcon(logo.get_icon())
        
        self.SetBackgroundColour('MEDIA GRAY')
        wx.StaticLine(parent=self.panel, id=-1, pos=(0, 0), size=(600, -1), 
                      style=wx.ALL|wx.EXPAND)
        
        #Basic Infos: Account + Help
        wx.StaticText(parent=self.panel, id=-1, label='Site Account:'+self.host_fetcher.username,
                      pos=(25, 5), size=(285, 25), style=wx.TE_RICH2)

        self.help_btn = platebtn.PlateButton(parent=self.panel, id=-1, label='Help?', 
                                         pos=(488, 2), size=(50, 25),
                                         style=platebtn.PB_STYLE_NOBG|platebtn.PB_STYLE_GRADIENT)
                                         
                
        #
        wx.StaticLine(parent=self.panel, id=-1, pos=(0, 30), size=(600, -1), 
                      style=wx.ALL|wx.EXPAND)
        
        #Path Setting
        self.path_setting_txt = wx.TextCtrl(parent=self.panel, id=-1, 
                                            value=self.store_path,
                                            pos=(23, 37), size=(370, 27),
                                            style=wx.TE_RICH2|wx.TE_READONLY)
        self.path_setting_txt.SetBackgroundColour(self.GetBackgroundColour())
        
        self.path_setting_btn = wx.Button(parent=self.panel, id=-1, 
                                          pos=(440, 35), size=(100, 30), 
                                          label='Path Setting')
        
        #
        wx.StaticLine(parent=self.panel, id=-1, pos=(0, 70), size=(600, -1), 
                      style=wx.ALL|wx.EXPAND)
        
        #WebSite + Account + Password
        wx.StaticText(parent=self.panel, id=-1, label='WebSite:', 
                      pos=(33, 84), size=(60, 25))
        self.website  = wx.Choice(parent=self.panel, id=-1, 
                                  pos=(98, 77), size=(200, 30),
                                  choices=SITE_CHOICES)
        self.website.SetSelection(0)
         
        wx.StaticText(parent=self.panel, id=-1, label='Account:',
                      pos=(32, 114), size=(60, 25))
        self.account  = wx.TextCtrl(parent=self.panel, id=-1, value='',
                                    pos=(98, 109), size=(200, 30))
          
        wx.StaticText(parent=self.panel, id=-1, label='Password:',
                      pos=(26, 151), size=(60, 25))
        self.password = wx.TextCtrl(parent=self.panel, id=-1, value='',
                                    pos=(98, 144), size=(200, 30), 
                                    style=wx.TE_PASSWORD)
         
        #Start
        self.start_btn = wx.Button(parent=self.panel, id=-1, label='Start',
                                   pos=(440, 135), size=(100, 30))
        
        #
        wx.StaticLine(parent=self.panel, id=-1, pos=(0, 180), size=(600, -1), 
                      style=wx.ALL|wx.EXPAND)
        
        #progress bar
        wx.RadioBox(parent=self.panel, id=-1, label='Progressing',
                                          pos=(20, 185), size=(518, 60),
                                          style=wx.RA_HORIZONTAL, choices=[''])
        self.progress_bar = wx.Gauge(parent=self.panel, id=-1, range=100, 
                                     pos=(25, 207), size=(508, 30),
                                     style=wx.GA_HORIZONTAL)
        self.progress_bar.SetValue(0)
        
        values = 'Running...\nCurrent User:' + self.host_fetcher.username + '\n'
        values += 'Current Version of Crawler:' + VERSION +'\n'
        self.logs_txt = wx.TextCtrl(parent=self.panel, id=-1, value=values,
                                    pos=(20, 255), size=(520, 230),
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
    
    def on_start(self, event):
        website  = SITE_CHOICES[self.website.GetCurrentSelection()]
        account  = self.account.GetValue().strip().encode('UTF-8')
        password = self.password.GetValue().strip().encode('UTF-8')
        
        if (account is None or len(account) == 0 or 
            password is None or len(password) == 0):
            wx.MessageBox(message='Account/Password cannot be blank. Please retry!',
                          caption='Warning', style=wx.OK|wx.ICON_INFORMATION)
            
            return
        
        #login
        if website == settings.SINA_WEIBO:
            fetcher = ComWeiboFetcher(username=account, password=password,
                                      window=self)
            
            if fetcher.check_cookie():
                crawler = StartCrawl(self.host_fetcher, website, fetcher, 
                                     self.store_path, self)
                crawler.start()
                self.panel.Enable(False)
                self.logs_txt.Enable(True)
                        
        elif website == settings.TWITTER:
            wx.MessageBox('Not Implemented')
        elif website == settings.FACEBOOK:
            wx.MessageBox('Not Implemented')
        
    def finished(self):
        self.panel.Enable(True)

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
            
    def on_taskbar(self, event):
        self.Show(False)
        self.tskbar.set()

    def update_progress_bar(self, count):
        self.progress_bar.SetValue(count)

    def on_close(self, event):
        ret = wx.MessageBox(message="Are you sure to exist?", style=wx.OK | wx.CANCEL)
        
        if ret == wx.OK:
            self.tskbar.RemoveIcon()
            self.tskbar.Destroy()
            self.Destroy()
            wx.GetApp().ExitMainLoop()
              
            os._exit(0)        

class Window(wx.App):
    def __init__(self, account_display=None):
        
        wx.App.__init__(self)
        self.frame = Frame(WIN_TITLE, WIN_STATUS, account_display)
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        
def main(*args, **kwargs):
    win = Window(*args, **kwargs)
    win.MainLoop()
       
if __name__ == '__main__':
    account_display = 'test'
    
    main(account_display=account_display) 