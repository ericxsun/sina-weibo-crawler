# encoding: utf-8


from sina_weibo.fetcher import ComWeiboFetcher
import sina_weibo
import sys
import time


user = ''
pwd  = ''
fetcher = ComWeiboFetcher(username=user, password=pwd)

login_ok = fetcher.check_cookie()

if not login_ok:
    print 'login failed.'
    sys.exit()
    
uids     = [1009809922, 1010112730, 1010112994, 1010189004, 1010258700, 
            1010279732, 1010303107, 1010571023, 1010634900, 1010659837, 
            1010812902]

msg_urls = ['http://weibo.com/1000000253/ezC36cq3i6G', 
            'http://weibo.com/1713926427/A2V5CENGU'] 


start = time.time()

sina_weibo.main(fetcher, fetch_data='weibos', store_path='./file/', uids=uids)

print 'crawl reposts and comments'
 
sina_weibo.main('local', fetcher, 'Infos', './file/', msg_urls=msg_urls)

cost_time = int(time.time() - start)
print 'finished: # connections: %s, cost time: %s' %(fetcher.n_connections, cost_time)