# encoding: utf-8
from sina_weibo.crawler import ComWeiboCrawler
from sina_weibo.fetcher import ComWeiboFetcher
import sys
import time

msg_url = 'http://weibo.com/1000000253/ezC36cq3i6G'
msg_id  = '10036505028'
page    = 1  
uid = 1000000253
# uid = 1039646267
# uid = 3079645245
# uid = 1043325954
# uid = 1806128454
# uid = 1002697421
# uid = 3087118795

store_path = './file/'

user = ''
pwd  = ''
fetcher = ComWeiboFetcher(username=user, password=pwd)

start = time.time()

login_ok = fetcher.check_cookie()

if not login_ok:
    print 'login failed.'
    sys.exit()

print 'crawl weibos'
crawler = ComWeiboCrawler(fetcher, store_path, uid=uid)
crawler.crawl_weibos()

print 'crawl follows'
crawler = ComWeiboCrawler(fetcher, store_path, uid=uid)
crawler.crawl_follows()
 
print 'crawl fans'
crawler = ComWeiboCrawler(fetcher, store_path, uid=uid)
crawler.crawl_fans()
 
print 'crawl infos'
crawler = ComWeiboCrawler(fetcher, store_path, uid=uid)
crawler.crawl_infos()
  
print 'crawl reposts'
crawler = ComWeiboCrawler(fetcher, store_path, msg_url=msg_url)
crawler.crawl_msg_reposts()
 
print 'crawl comments'
crawler = ComWeiboCrawler(fetcher, store_path, msg_url=msg_url)
crawler.crawl_msg_comments()

cost_time = int(time.time() - start)    

print 'finished: # connections: %s, cost time: %s' %(fetcher.n_connections, cost_time)