# encoding: utf-8

from common import STORE_PATH, write_message, logger, update_progress_bar, \
                    format_delta_time
from crawler import ComWeiboCrawler
from storage import FileStorage
import settings
import time

def main(fetcher, **kwargs):
    fetch_data = kwargs.get('fetch_data', None)
    uids       = kwargs.get('uids', None)
    msg_urls   = kwargs.get('msg_urls', None)
    store_path = kwargs.get('store_path', STORE_PATH)
    window     = kwargs.get('window', None)
    
    assert (fetch_data is not None and uids is not None) or (msg_urls is not None)
    
    n_ids = 0
    
    start_time = time.time()
    last_time  = start_time
    
    n_connections = 0
    
    if uids is not None:
        fetch_data = fetch_data.lower()
        n_ids  = len(uids)
        
        write_message(('=======Need to crawl: uids-%d======='  %n_ids), window)
        i = 0
        
        for uid in uids:
            fetcher.n_connections = 0
            
            if i > 0:
                sec = 60
                msg  = '-------\n'
                msg += 'Take a rest: %d seconds, and start new crawler..' %sec
                
                write_message(msg, window)
                time.sleep(sec)
            
            now_time = time.time()
            dt = int(now_time - last_time)
            if dt >= 3600:
                msg = 'Having Crawled for %d seconds, take a rest: 1 hours' %dt
                logger.info(msg)
                write_message(msg, window)
                
                time.sleep(3600)
                
                last_time = time.time()
            
            if fetch_data == 'weibos':
                crawler = ComWeiboCrawler(fetcher, store_path, uid=uid, window=window)
                crawler.crawl_weibos()
            elif fetch_data == 'follows':
                crawler = ComWeiboCrawler(fetcher, store_path, uid=uid, window=window)
                crawler.crawl_follows()
            elif fetch_data == 'fans':
                crawler = ComWeiboCrawler(fetcher, store_path, uid=uid, window=window)
                crawler.crawl_fans()
            elif fetch_data == 'infos':
                crawler = ComWeiboCrawler(fetcher, store_path, uid=uid, window=window)
                crawler.crawl_infos()
    
            i += 1
            
            update_progress_bar(window, i*100/n_ids)
            
            n_connections += fetcher.n_connections   
            
    elif msg_urls is not None:
        n_ids = len(msg_urls)
        
        write_message(('=======Need to crawl: messages-%d======='  %n_ids), window)
        i = 0
        
        for msg_url in msg_urls:
            fetcher.n_connections = 0
            
            if i > 0:
                sec = 60
                msg = 'Take a rest: %d seconds, and start new crawler..' %sec
                
                write_message(msg, window)
                time.sleep(sec)

            now_time = time.time()
            dt = int(now_time - last_time)
            if dt >= 3600:
                msg = 'Having Crawled for %d seconds, take a rest: 1 hours' %dt
                logger.info(msg)
                write_message(msg, window)
                
                time.sleep(3600)
                
                last_time = time.time()
            
            if not msg_url.startswith('http://weibo.com/'):
                msg_url = 'http://weibo.com/' + msg_url.replace('/', '')
            
            #repost
            crawler = ComWeiboCrawler(fetcher, store_path, msg_url=msg_url, window=window)
            crawler.crawl_msg_reposts()
            
            sec = 10
            msg = 'Take a rest: [%d]sec, and start to crawl the comments..' %sec
            write_message(msg, window)
            time.sleep(sec)
            
            #comment
            crawler = ComWeiboCrawler(fetcher, store_path, msg_url=msg_url, window=window)
            crawler.crawl_msg_comments()
    
            i += 1
            
            update_progress_bar(window, i*100/n_ids)
            
            n_connections += fetcher.n_connections
        
    cost_time = int(time.time() - start_time)
    
    d, h, m, s = format_delta_time(cost_time)
    msg  = 'The task has successfully finished.\n'
    msg += 'Crawled [user|message]ids: %d, cost time: %d(d)-%d(h)-%d(m)-%d(s), connections: %d' %(n_ids, d, h, m, s, n_connections)
    
    write_message('=======', window)
    logger.info(msg)
    write_message(msg, window)