# encoding: utf-8

from sina_weibo.fetcher import CnWeiboFetcher
from sina_weibo.fetcher import ComWeiboFetcher
import sina_weibo
import sys
import time

def TestWeibo__init__(user, pwd, weibo_com):
    
    if weibo_com:
        fetcher = ComWeiboFetcher(username=user, password=pwd)
    else:
        fetcher = CnWeiboFetcher(username=user, password=pwd)

    login_ok = fetcher.check_cookie()
    if not login_ok:
        print 'login failed.'
        sys.exit()
        
    uids = [1000000253, 10057, 10029]
    
    msg_urls = ['http://weibo.com/1000000253/ezC36cq3i6G', 
                'http://weibo.com/1713926427/A2V5CENGU'] 
    
    start = time.time()
    
    if weibo_com:
        print 'crawl weibos'
        sina_weibo.main(fetcher, fetch_data='weibos', store_path='./file/', uids=uids)
        
        print 'crawl infos'
        sina_weibo.main(fetcher, fetch_data='infos', store_path='./file/', uids=uids)
        
        print 'crawl reposts'
        sina_weibo.main(fetcher, store_path='./file/', msg_urls=msg_urls, fetch_data='repost')
        
        print 'crawl comments'
        sina_weibo.main(fetcher, store_path='./file/', msg_urls=msg_urls, fetch_data='comment')
    
    print 'crawl follows'
    sina_weibo.main(fetcher, fetch_data='follows', store_path='./file/', uids=uids)
    
    print 'crawl fans'
    sina_weibo.main(fetcher, fetch_data='fans', store_path='./file/', uids=uids)
    
    cost_time = int(time.time() - start)
    print 'finished: # connections: %s, cost time: %s' %(fetcher.n_connections, cost_time)

if __name__ == '__main__':
    user = ''
    pwd  = ''
    
    TestWeibo__init__(user, pwd, weibo_com=True)