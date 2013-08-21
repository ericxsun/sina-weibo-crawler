# encoding: utf-8

from pyquery import PyQuery as pq
from sina_weibo import settings
from sina_weibo.parser import ComWeibosParser, ComFollowsParser, ComFansParser,\
                               ComRepostsParser, ComCommentsParser, ComInfosParser
from sina_weibo.storage import FileStorage
import codecs

msg_url = 'http://weibo.com/1000000253/ezC36cq3i6G'
msg_id  = '10036505028'
page    = 1  
uid = 1039646267
# uid = 3079645245
# uid = 1043325954
# uid = 1806128454
# uid = 1002697421
# uid = 3087118795

f_weibos  = './file/weibos-%s.txt'   %(uid)
f_follows = './file/follows-%s.txt'  %(uid)
f_fans    = './file/fans-%s.txt'     %(uid)
f_infos   = './file/infos-%s.txt'    %(uid)
f_reposts = './file/reposts-%s.txt'  %(msg_id)
f_comments= './file/comments-%s.txt' %(msg_id)

print 'test for ComWeiboParser...'
storage = FileStorage(uid, settings.MASK_WEIBO, './file/')
html = codecs.open(f_weibos, 'r', 'utf-8').read()
parser = ComWeibosParser(uid, storage)
try:
    pq_doc = pq(html)
    print 'page count: %d' %(parser.parse(pq_doc))
except:
    print html
    
print 'test for ComFollowsParser...'
storage = FileStorage(uid, settings.MASK_FOLLOW, './file/')
html = codecs.open(f_follows, 'r', 'utf-8').read()
parser = ComFollowsParser(storage)
try:
    pq_doc = pq(html)
    print 'page count: %d' %(parser.parse(pq_doc))
except:
    print html
    
print 'test for ComFansParser...'
storage = FileStorage(uid, settings.MASK_FAN, './file/')
html = codecs.open(f_fans, 'r', 'utf-8').read()
parser = ComFansParser(storage)
try:
    pq_doc = pq(html)
    print 'page count: %d' %(parser.parse(pq_doc))
except:
    print html
    
print 'test for ComInfosParser...'
storage = FileStorage(uid, settings.MASK_INFO, './file/')
html = codecs.open(f_infos, 'r', 'utf-8').read()
parser = ComInfosParser(uid, storage)
try:
    pq_doc = pq(html)
    parser.parse(pq_doc)
except:
    print html
    
print 'test for ComRepostsParser...'
storage = FileStorage(msg_id, settings.MASK_REPOST, './file/')
html = codecs.open(f_reposts, 'r', 'utf-8').read()
parser = ComRepostsParser(msg_id, storage)
try:
    pq_doc = pq(html)
    parser.parse(pq_doc)
except:
    print html
     
print 'test for ComCommentsParser...'
storage = FileStorage(msg_id, settings.MASK_COMMENT, './file/')
html = codecs.open(f_comments, 'r', 'utf-8').read()
parser = ComCommentsParser(msg_id, storage)
try:
    pq_doc = pq(html)
    parser.parse(pq_doc)
except:
    print html       