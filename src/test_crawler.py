# encoding: utf-8
from sina_weibo.crawler import CnWeiboCrawler
from sina_weibo.crawler import ComWeiboCrawler
from sina_weibo.fetcher import CnWeiboFetcher
from sina_weibo.fetcher import ComWeiboFetcher
import sys
import time

def TestComWeiboCrawler(user, pwd):
    
    # uid = 1039646267
    # uid = 3079645245
    # uid = 1043325954
    # uid = 1806128454
    # uid = 1002697421
    # uid = 3087118795
    # uid = 3045056321
    # uid = 3104811705
    # uid = 2901331743
    # uid = 1021
    # uid = 3207638224
    uid = 1000000253

    msg_url = 'http://weibo.com/1000000253/ezC36cq3i6G' #msg_id  = '10036505028'

    store_path = './file/'

    fetcher = ComWeiboFetcher(username=user, password=pwd)

    start = time.time()
    
    login_ok = fetcher.check_cookie()
    
    if not login_ok:
        print 'login failed.'
        sys.exit()
    
    fetcher.n_connections = 0
    print 'crawl weibos'
    crawler = ComWeiboCrawler(fetcher, store_path, uid=uid)
    crawler.crawl_weibos()
    
    fetcher.n_connections = 0
    print 'crawl follows'
    crawler = ComWeiboCrawler(fetcher, store_path, uid=uid)
    crawler.crawl_follows()
     
    fetcher.n_connections = 0
    print 'crawl fans'
    crawler = ComWeiboCrawler(fetcher, store_path, uid=uid)
    crawler.crawl_fans()
    
    fetcher.n_connections = 0
    print 'crawl infos'
    crawler = ComWeiboCrawler(fetcher, store_path, uid=uid)
    crawler.crawl_infos()
    
    fetcher.n_connections = 0
    print 'crawl reposts'
    crawler = ComWeiboCrawler(fetcher, store_path, msg_url=msg_url)
    crawler.crawl_msg_reposts()
     
    fetcher.n_connections = 0
    print 'crawl comments'
    crawler = ComWeiboCrawler(fetcher, store_path, msg_url=msg_url)
    crawler.crawl_msg_comments()
    
    cost_time = int(time.time() - start)    
    
    print 'finished: # connections: %s, cost time: %s' %(fetcher.n_connections, cost_time)
    
def TestCnWeiboCrawler(user, pwd):
    
    uid = 10029
    # uid = 10057
    # uid = 10111
    # uid = 10145
    # uid = 10211
    # uid = 10318
    # uid = 10361
    # uid = 10392

    store_path = './file/'

    fetcher = CnWeiboFetcher(username=user, password=pwd)

    start = time.time()
    
    login_ok = fetcher.check_cookie()
    
    if not login_ok:
        print 'login failed.'
        sys.exit()
    
    fetcher.n_connections = 0
    print 'crawl follows'
    crawler = CnWeiboCrawler(fetcher, store_path, uid=uid)
    crawler.crawl_follows()
    
    fetcher.n_connections = 0
    print 'crawl fans'
    crawler = CnWeiboCrawler(fetcher, store_path, uid=uid)
    crawler.crawl_fans()
     
    cost_time = int(time.time() - start)    
    
    print 'finished: # connections: %s, cost time: %s' %(fetcher.n_connections, cost_time)
    
if __name__ == '__main__':
    user = ''
    pwd  = ''
    
    print 'Test for weibo.com crawler...'
    TestComWeiboCrawler(user, pwd)
    
    print 'Test for weibo.cn crawler...'
    TestCnWeiboCrawler(user, pwd)