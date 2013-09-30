# encoding: utf-8

import Queue
import sys
import threading

class Worker(threading.Thread):
    def __init__(self, worker_manager, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.setDaemon(True)
        
        self.worker_manager = worker_manager
        self.timeout = worker_manager.timeout
        self.state = None
        
        self.start()
    
    def run(self):
        while True:
            if self.state == 'STOP':
                break
            
            try:
                func, args, kwargs = self.worker_manager.work_queue.get(timeout=self.timeout)
                
                res = func(*args, **kwargs)

                if res is None:
                    self.worker_manager.res_is_None = True
                    self.state = 'STOP'
                    self.worker_manager.stop()
                
                self.worker_manager.work_queue.task_done()
            except Queue.Empty:
                break
            except Exception, e:
                print e
                print sys.exc_info()[:2]
                break

    def stop(self):
        self.state = 'STOP'

class WorkerManager(object):
    def __init__(self, num_workers=5, timeout=1):
        self.work_queue = Queue.Queue()
        self.res_is_None = False
        
        self.workers = []
        self.timeout = timeout
        self.recruit_threads(num_workers)
        
    def recruit_threads(self, num_workers):
        for _ in range(num_workers):
            worker = Worker(self)
            self.workers.append(worker)
    
    def add_job(self, func, *args, **kwargs):
        self.work_queue.put((func, args, kwargs))
            
    def wait_all_complete(self):
        for worker in self.workers:
            if worker.isAlive():
                worker.join()

    def work_done(self):
        self.work_queue.task_done()
        
    def get_result(self, *args, **kwargs):
        return self.res_is_None
    
    def stop(self):
        for worker in self.workers:
            worker.stop()
            
        del self.workers[:]