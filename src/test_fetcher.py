# encoding: utf-8

from sina_weibo import settings
from sina_weibo.fetcher import CnWeiboFetcher
from sina_weibo.fetcher import ComWeiboFetcher
import codecs
import time

def TestComWeiboFetcher(user, pwd):

    uid = 1039646267
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

    page = 1
    
    msg_id  = '10036505028'
    msg_url = 'http://weibo.com/1000000253/ezC36cq3i6G'

    f_weibos  = './file/weibos-%s.txt'   %(uid)
    f_follows = './file/follows-%s.txt'  %(uid)
    f_fans    = './file/fans-%s.txt'     %(uid)
    f_infos   = './file/infos-%s.txt'    %(uid)
    f_reposts = './file/reposts-%s.txt'  %(msg_id)
    f_comments= './file/comments-%s.txt' %(msg_id)
    
    #-------------------------------------------
    start = time.time()
    
    fetcher = ComWeiboFetcher(username=user, password=pwd)
    
    print 'test for check cookie weibo.com'
    print fetcher.check_cookie()
    
    print 'test for check user exist...'
    print fetcher.check_user(uid)
     
    print 'test for check message exist...'
    print fetcher.check_message(msg_url)
     
    print 'test for fetch weibo...'
    html = fetcher.fetch_weibo(uid=uid, page=page)
    with codecs.open(f_weibos, 'w', 'utf-8') as f:
        f.write(html)
     
    print 'test for fetch follows...'
    url = 'http://weibo.com/%s/follow?page=%s' % (uid, page)
    html = fetcher.fetch(url, settings.QUERY_FOLLOWS)
    with codecs.open(f_follows, 'w', 'utf-8') as f:
        f.write(html)
      
    print 'test for fetch fans...'
    url = 'http://weibo.com/%s/fans?page=%s' % (uid, page)
    html = fetcher.fetch(url, settings.QUERY_FANS)
    with codecs.open(f_fans, 'w', 'utf-8') as f:
        f.write(html)
          
    print 'test for fetch infos...'
    url = 'http://weibo.com/%s/info' % uid
    html = fetcher.fetch(url, settings.QUERY_INFO)
    with codecs.open(f_infos, 'w', 'utf-8') as f:
        f.write(html)
                         
    print 'test for fetch message repost'
    html, page_cnt = fetcher.fetch_msg_reposts(msg_id, page)
    print 'total page: %s' %page_cnt
    with codecs.open(f_reposts, 'w', 'utf-8') as f:
        f.write(html)
                        
    print 'test for fetch message comment'
    html, page_cnt = fetcher.fetch_msg_comments(msg_id, page)
    print 'total page: %s' %page_cnt
    with codecs.open(f_comments, 'w', 'utf-8') as f:
        f.write(html)
    
    cost_time = int(time.time() - start)    
    
    print 'finished: # connections: %s, cost time: %s' %(fetcher.n_connections, cost_time)
    
def TestCnWeiboFetcher(user, pwd):

    uid = 10029
#     uid = 10057
#     uid = 10111
#     uid = 10145
#     uid = 10211
#     uid = 10318
#     uid = 10361
#     uid = 10392

    page = 1

    f_weibos  = './file/weibos-%s.txt'   %(uid)
    f_follows = './file/follows-%s.txt'  %(uid)
    f_fans    = './file/fans-%s.txt'     %(uid)
    f_infos   = './file/infos-%s.txt'    %(uid)
    
    #-------------------------------------------
    start = time.time()
    
    fetcher = CnWeiboFetcher(username=user, password=pwd)
    
    print 'test for check cookie weibo.com'
    print fetcher.check_cookie()
    
    print 'test for check user exist...'
    print fetcher.check_user(uid)
     
    print 'test for fetch weibo...'
    url = 'http://weibo.cn/%s?page=%s' % (uid, page)
    html = fetcher.fetch(url)
    with codecs.open(f_weibos, 'w', 'utf-8') as f:
        f.write(html)
     
    print 'test for fetch follows...'
    url = 'http://weibo.cn/%s/follow?page=%s' % (uid, page)
    html = fetcher.fetch(url)
    with codecs.open(f_follows, 'w', 'utf-8') as f:
        f.write(html)
      
    print 'test for fetch fans...'
    url = 'http://weibo.cn/%s/fans?page=%s' % (uid, page)
    html = fetcher.fetch(url)
    with codecs.open(f_fans, 'w', 'utf-8') as f:
        f.write(html)
          
    print 'test for fetch infos...'
    url = 'http://weibo.cn/%s/info' % uid
    html = fetcher.fetch(url)
    with codecs.open(f_infos, 'w', 'utf-8') as f:
        f.write(html)
    
    cost_time = int(time.time() - start)    
    
    print 'finished: # connections: %s, cost time: %s' %(fetcher.n_connections, cost_time)

if __name__ == '__main__':
    user = 'ssh2222@qq.com'
    pwd  = '2222ssh'
    
    print 'Test for weibo.cn fetcher...'
#     TestCnWeiboFetcher(user, pwd)
    
    print 'Test for weibo.com fetcher...'
    TestComWeiboFetcher(user, pwd)
