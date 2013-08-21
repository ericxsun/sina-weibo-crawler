# encoding: utf-8

class AutoThrottel(object):
    def __init__(self, fetcher):
        self.fetcher = fetcher
        
    
    def _min_delay(self, spider):
        pass  
        
        
    def _get_slot(self, request, fetcher):
        pass
        
    def _adjust_delay(self, slot, latency, response):
        '''define delay adjustment policy'''
        pass
    