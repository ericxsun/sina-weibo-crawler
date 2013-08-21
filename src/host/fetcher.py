# coding: utf-8

import settings

class HostFetcher(object):
    def __init__(self, username, password, **kwargs):
        self.host = settings.HOST
        self.port = settings.PORT
        
        self.username = username
        self.password = password
        
        self.window = kwargs.get('window', None)
    
    
    def login(self, login_user=None, login_pwd=None):
        if login_user is None or login_pwd is None:
            login_user = self.username
            login_pwd  = self.password
        
        assert(login_user is not None and login_pwd is not None)
        
        login_ok = False
        
        #send the version for update client
    
    def request_task(self):
        task_id = None
        
        return task_id
    
    def upload_task(self, file):
        upload_flag = False
        
        return upload_flag
    