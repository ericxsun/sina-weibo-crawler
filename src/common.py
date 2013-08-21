# encoding: utf-8

import logging
import os
import sys
import time
import traceback
import wx
    
if getattr(sys, 'frozen', False):
    PATH = os.path.dirname(sys.executable)
elif __file__:
    PATH = os.path.dirname(__file__)

SOFT_PATH = PATH
TASK_PATH = PATH
  
STORE_PATH = os.path.join(PATH, 'file')
if not os.path.exists(STORE_PATH):
    os.makedirs(STORE_PATH)
            
class FixedLogger(logging.Logger):
    def exception(self, msg, *args):
        '''
        Convenience method for logging an ERROR with exception information.
        '''
        self.error(msg, exc_info=1, *args)
        
def get_logger(filename):
    logger = FixedLogger(logging.getLogger('crawler'))
        
    handler   = logging.FileHandler(filename)
    formatter = logging.Formatter(fmt=('%(asctime)s-%(module)s.%(funcName)s.'
                                       '%(lineno)d-%(levelname)s-%(message)s'))
        
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
        
    logger.addHandler(handler)
                
    return logger

if getattr(sys, 'frozen', False):
    LOG_PATH = os.path.dirname(sys.executable)
elif __file__:
    LOG_PATH = os.path.dirname(__file__)

T = time.strftime('%Y-%m-%d-%H-%M', time.localtime())   
logger = get_logger(os.path.join(LOG_PATH, 'run-'+T+'.log'))

def write_message(msg, window=None):
    if window is None:
        sys.stdout.write(msg+'\n')
    else:
        try:
            wx.CallAfter(window.write_logs, str(msg))
        except AttributeError:
            wx.MessageBox(msg)

def finish_task(window=None):
    try:
        wx.CallAfter(window.finished)
    except:
        pass

def update_progress_bar(window, val):
    try:
        wx.CallAfter(window.update_progress_bar, val)
    except AttributeError:
        pass

def format_delta_time(dt):
    s  = dt % 60
    dt = dt // 60
    
    m  = dt % 60
    dt = dt // 60
    
    h  = dt % 60
    dt = dt // 60
    
    return dt, h, m, s 

def record_traceback(file_name):
    try:
        f = open(file_name, 'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
    except:
        pass
