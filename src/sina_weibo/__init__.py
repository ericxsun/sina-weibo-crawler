# encoding: utf-8

from __future__ import division
from common import STORE_PATH, write_message, logger, update_progress_bar, \
                    format_delta_time
from crawler import ComWeiboCrawler
from sina_weibo.crawler import CnWeiboCrawler
from storage import FileStorage
import codecs
import os
import random
import settings
import time

def adjust_delay(dt):
    '''
    delay: 5 ranks
    '''
    
    if dt <= 10:
        delay = random.randint(1, 5)
    elif dt <= 60:
        delay = random.randint(5, 10)
    elif dt <= 300:
        delay = random.randint(10, 30)
    elif dt <= 600:
        delay = random.randint(30, 60)
    else:
        delay = random.randint(60, 300)
        
    return delay

def main(fetcher, **kwargs):
    fetch_data = kwargs.get('fetch_data', None)
    uids       = kwargs.get('uids', None)
    msg_urls   = kwargs.get('msg_urls', None)
    store_path = kwargs.get('store_path', STORE_PATH)
    window     = kwargs.get('window', None)
    weibo_com  = kwargs.get('weibo_com', True)
    
    fetcher.window = window
    
    assert (fetch_data is not None and uids is not None) or (msg_urls is not None)
    
    n_ids = 0
    n_connections = 0
    n_errors = 0
    
    succeed_fp   = codecs.open(os.path.join(store_path, 'succeed-id.txt'),   'w+', 'utf-8')
    error_fp     = codecs.open(os.path.join(store_path, 'error-id.txt'),     'w+', 'utf-8')
    not_exist_fp = codecs.open(os.path.join(store_path, 'not-exist-id.txt'), 'w+', 'utf-8')
    
    start_time = time.time()
    
    if weibo_com:
        if uids is not None:
            fetch_data = fetch_data.lower()
            n_ids      = len(uids)
            
            write_message(('=======Need to crawl: uids-%d======='  %n_ids), window)
            
            i     = 0
            dt_id = 0
            
            for uid in uids:
                fetcher.n_connections = 0
                
                if dt_id > 0:
                    delay = adjust_delay(dt_id)
                    msg  = '-------\n'
                    msg += 'Take a rest: %d seconds, and start new crawler..' %delay
                    msg += '\n-------'
                
                    write_message(msg, window)
                    time.sleep(delay)
            
                t_id_s = time.time()
                
                if fetch_data == 'weibos':
                    crawler = ComWeiboCrawler(fetcher, store_path, uid=uid, window=window)
                
                    res = crawler.crawl_weibos()
                    if res is None:
                        n_errors += 1
                        error_fp.write(str(uid) + '\n')
                    elif res is False:
                        not_exist_fp.write(str(uid) + '\n')
                    elif res is True:
                        succeed_fp.write(str(uid) + '\n')
                elif fetch_data == 'follows':
                    crawler = ComWeiboCrawler(fetcher, store_path, uid=uid, window=window)
                    
                    res = crawler.crawl_follows()
                    if res is None:
                        n_errors += 1
                        error_fp.write(str(uid) + ';')
                    elif res is False:
                        not_exist_fp.write(str(uid) + ';')
                    elif res is True:
                        succeed_fp.write(str(uid) + ';')
                elif fetch_data == 'fans':
                    crawler = ComWeiboCrawler(fetcher, store_path, uid=uid, window=window)
                    
                    res = crawler.crawl_fans()
                    if res is None:
                        n_errors += 1
                        error_fp.write(str(uid) + ';')
                    elif res is False:
                        not_exist_fp.write(str(uid) + ';')
                    elif res is True:
                        succeed_fp.write(str(uid) + ';')
                elif fetch_data == 'infos':
                    crawler = ComWeiboCrawler(fetcher, store_path, uid=uid, window=window)
                    
                    res = crawler.crawl_infos()
                    if res is None:
                        n_errors += 1
                        error_fp.write(str(uid) + ';')
                    elif res is False:
                        not_exist_fp.write(str(uid) + ';')
                    elif res is True:
                        succeed_fp.write(str(uid) + ';')
                
                #--
                t_id_e = time.time()
                dt_id  = int(t_id_e - t_id_s)
                
                i += 1
                
                update_progress_bar(window, i*100/n_ids)
                
                n_connections += fetcher.n_connections
            
            #--end for uid in uids  
                    
        elif msg_urls is not None:
            n_ids = len(msg_urls)
            
            write_message(('=======Need to crawl: messages-%d======='  %n_ids), window)
            
            i     = 0
            dt_id = 0
            
            for msg_url in msg_urls:
                fetcher.n_connections = 0
                
                if not msg_url.startswith('http://weibo.com/'):
                    msg_url = 'http://weibo.com/' + msg_url.replace('/', '')
                
                if dt_id > 0:
                    delay = adjust_delay(dt_id)
                    msg  = '-------\n'
                    msg += 'Take a rest: %d seconds, and start new crawler..' %delay
                    msg += '\n-------'
                    
                    write_message(msg, window)
                    time.sleep(delay)
                
                t_id_s = time.time()
                
                #repost
                if fetch_data == 'repost':
                    crawler = ComWeiboCrawler(fetcher, store_path, msg_url=msg_url, window=window)
                    
                    res = crawler.crawl_msg_reposts()
                    if res is None:
                        n_errors += 1
                        error_fp.write(str(msg_url) + ';')
                    elif res is False:
                        not_exist_fp.write(str(msg_url) + ';')
                    elif res is True:
                        succeed_fp.write(str(msg_url) + ';')
                
                #comment    
                elif fetch_data == 'comment':           
                    crawler = ComWeiboCrawler(fetcher, store_path, msg_url=msg_url, window=window)
                    
                    res = crawler.crawl_msg_comments()
                    if res is None:
                        n_errors += 1
                        error_fp.write(str(msg_url) + ';')
                    elif res is False:
                        not_exist_fp.write(str(msg_url) + ';')
                    elif res is True:
                        succeed_fp.write(str(msg_url) + ';')
                
                #--
                t_id_e = time.time()
                dt_id  = int(t_id_e - t_id_s)
                
                i += 1
                
                update_progress_bar(window, i*100/n_ids)
                
                n_connections += fetcher.n_connections
            
            #--end for msg_url in msg_urls
    
    else:   #weibo.cn
        if uids is not None:
            fetch_data = fetch_data.lower()
            n_ids      = len(uids)
            
            write_message(('=======Need to crawl: uids-%d======='  %n_ids), window)
            
            i     = 0
            dt_id = 0
            
            for uid in uids:
                fetcher.n_connections = 0
                
                if dt_id > 0:
                    delay = adjust_delay(dt_id)
                    msg  = '-------\n'
                    msg += 'Take a rest: %d seconds, and start new crawler..' %delay
                    msg += '\n-------'
                
                    write_message(msg, window)
                    time.sleep(delay)
            
                t_id_s = time.time()
                
                if fetch_data == 'follows':
                    crawler = CnWeiboCrawler(fetcher, store_path, uid=uid, window=window)
                    
                    res = crawler.crawl_follows()
                    if res is None:
                        n_errors += 1
                        error_fp.write(str(uid) + ';')
                    elif res is False:
                        not_exist_fp.write(str(uid) + ';')
                    elif res is True:
                        succeed_fp.write(str(uid) + ';')
                elif fetch_data == 'fans':
                    crawler = CnWeiboCrawler(fetcher, store_path, uid=uid, window=window)
                    
                    res = crawler.crawl_fans()
                    if res is None:
                        n_errors += 1
                        error_fp.write(str(uid) + ';')
                    elif res is False:
                        not_exist_fp.write(str(uid) + ';')
                    elif res is True:
                        succeed_fp.write(str(uid) + ';')
                
                #--
                t_id_e = time.time()
                dt_id  = int(t_id_e - t_id_s)
                
                i += 1
                
                update_progress_bar(window, i*100/n_ids)
                
                n_connections += fetcher.n_connections
            
            #--end for uid in uids
        #--
    succeed_fp.close()
    error_fp.close()
    not_exist_fp.close()    
    
    cost_time = int(time.time() - start_time)
        
    d, h, m, s = format_delta_time(cost_time)
    msg  = 'The task has successfully finished.\n'
    msg += 'Crawled [user|message]ids: %d, cost time: %d(d)-%d(h)-%d(m)-%d(s), connections: %d' %(n_ids, d, h, m, s, n_connections)
    
    accuracy = 1 - n_errors / n_ids if n_ids > 0 else 0
    msg += '\nAccuracy:%d%%' %(accuracy*100)
        
    write_message('=======', window)
    logger.info(msg)
    write_message(msg, window)
        
    return accuracy
    