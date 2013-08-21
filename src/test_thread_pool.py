# encoding: utf-8

from src.thread_pool import WorkerManager
import sys
import time

def do_job(msg):
    sys.stdout.write(msg)
    time.sleep(5)
    
    
if __name__ == '__main__':
    st = time.time()
    wm = WorkerManager(5, 5)
    for i in range(1000):
        msg = 'start:%s, sleep 5sec\n' %i
        wm.add_job(do_job, msg)
    wm.wait_all_complete()
    ed = time.time()
    
    print 'cost time: %s' %(ed - st)
