# encoding: utf-8

from thread_pool import WorkerManager
# import sys
import time

def do_job(msg):
#     sys.stdout.write(msg)
#     print 'in do job:', msg
    return msg
    
    
if __name__ == '__main__':
    st = time.time()
    wm = WorkerManager(5, 5)
    
    wm.add_job(do_job, None)
    
    for i in range(1, 100):
        wm.add_job(do_job, i)
    
    wm.wait_all_complete()
    res = wm.get_result()
    wm.stop()
    print 'res:', res
    ed = time.time()
    
    print 'cost time: %s' %(ed - st)
