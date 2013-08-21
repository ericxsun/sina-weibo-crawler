# encoding: utf-8

import Queue
import sys
import threading

class Worker(threading.Thread):
    def __init__(self, work_queue, timeout=1, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.setDaemon(True)
        
        self.work_queue = work_queue
        self.timeout    = timeout
        
        self.start()
    
    def run(self):
        while True:
            try:
                func, args, kwargs = self.work_queue.get(timeout=self.timeout)
                
                func(*args, **kwargs)
                
                self.work_queue.task_done()
            except Queue.Empty:
                break
            except Exception, e:
                print e
                print sys.exc_info()[:2]
                break

class WorkerManager(object):
    def __init__(self, num_workers=5, timeout=1):
        self.work_queue = Queue.Queue()
        self.workers = []
        self.timeout = timeout
        self.recruit_threads(num_workers)
        
    def recruit_threads(self, num_workers):
        for _ in range(num_workers):
            worker = Worker(self.work_queue, self.timeout)
            self.workers.append(worker)
    
    def add_job(self, func, *args, **kwargs):
        self.work_queue.put((func, args, kwargs))
            
    def wait_all_complete(self):
        for worker in self.workers:
            if worker.isAlive():
                worker.join()