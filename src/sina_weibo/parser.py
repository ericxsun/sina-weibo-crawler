# encoding: utf-8

from pyquery import PyQuery as pq
from threading import Lock  # added for datetime.strptime is not thread-safe
import datetime
import settings
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

class ComWeibosParser(object):
    def __init__(self, uid, storage):
        self.uid     = uid
        self.storage = storage
        
    def parse(self, pq_doc):
        def _parse_msg(node):
            '''
            <div class="WB_text" node-type="feed_list_[content|reason]">
                abcdefg***<img **>....
            </div>
            '''
            
            return node.text()
        
        def _parse_media(node):
            '''
            <ul class="WB_meida_list clearfix" nodet-type="feed_list_media_prev">
                ???
            </ul>
            or 
            <div node-type="feed_list_media_prev">
                <ul class="WB_media_list clearfix">
                    ???
                </ul>
            </div>
            
            current version: not extract the detail information of medias
            '''
            
            return (node.html() is not None)
        
        def _parse_map(node):
            '''
            <div class="map_data">
                <span  class="W_ico16 icon_locate"></span>
                ???
                <a action-data="??" action-type="feed_list_geo_info" href="??">显示地图</a>
            </div>
            '''
            try:
                return node.text().split('-')[0].strip().replace(',', '-')
            except AttributeError:
                return None
        
        def _parse_from(node):
            '''
            <div class="WB_from">
                <a class="S_link2 WB_time" href="/uid/shorturl" title="time">**</a>
                <a class="S_link2" rel="nofollow" **>**</a>
            </div>
            '''
            
            url_a   = node.children('a[node-type="feed_list_item_date"]')
            msgurl  = 'http://weibo.com' + url_a.attr('href')
            msgtime = url_a.attr('date')[0:10]
            msgfrom = node.children('a[rel="nofollow"]').text()

            return msgurl, msgtime, msgfrom
        
        def _parse_handle(node):
            '''
            <div class="WB_handle">
                <a action-type="feed_list_like">(??)</a>
                <a action-type="feed_list_forward">转发(??)</a>
                <a action-type="feed_list_favorite">收藏(??)</a>
                <a action-type="feed_list_comment">评论(??)</a>
            </div>
            '''
            
            n_likes    = '0'
            n_forwards = '0'
            n_favorites= '0'
            n_comments = '0'
            
            st = node.text()
            if st is not None and len(st) > 0:
                st = st.split('|')
                for s in st:
                    if s is not None and '(' in s:
                        s = s.strip()
                         
                        if len(s.split('(')[0]) == 0:
                            n_likes = s.split('(')[-1].strip(')')
                        elif s.split('(')[0] == u'转发':
                            n_forwards = s.split('(')[-1].strip(')')
                        elif s.split('(')[0] == u'收藏':
                            n_favorites = s.split('(')[-1].strip(')')
                        elif s.split('(')[0] == u'评论':
                            n_comments = s.split('(')[-1].strip(')')       
             
            return n_likes, n_forwards, n_favorites, n_comments
        
        def _parse_msg_id(node):
            '''
            <div class="WB_handle">
                <a action-type="feed_list_like" action-data=".&mid=*&">(??)</a>
                ...
            </div>
            '''
            
            a = node.find('a[action-type="feed_list_like"]')
            try:
                return a.attr('action-data').split('&mid=')[-1].split('&')[0]
            except:
                return ''
            
        def _parse_forward_info(node):
            '''
            <div class="WB_info">
                <a class="WB_name S_func3" nick-name="??" usercard="id=??" node-type="feed_list_originNick">??</a>
                <a href="???">??</a>
            </div>
            '''
            info = {
                'forward_uid': '', 'forward_nickname': '', 'forward_daren': '',
                'forward_verified': '', 'forward_vip': ''
            }

            info_a = node.children('a')
            for a in info_a:
                a = pq(a)
                    
                if a.attr('node-type') == 'feed_list_originNick':
                    info['forward_uid']      = a.attr('usercard').split('id=')[-1]
                    info['forward_nickname'] = a.attr('nick-name')
                elif a.attr('href').startswith('http://club.weibo.com/'):
                    info['forward_daren'] = a.children('i.W_ico16.ico_club').attr('title')
                elif a.attr('href').startswith('http://verified.weibo.com/'):
                    info['forward_verified'] = a.children('i.W_ico16.approve').attr('title')
                elif a.attr('href').startswith('http://vip.weibo.com'):
                    info['forward_vip'] = a.attr('title')
            
            return info
            
        def _parse_forward(node):
            '''
            <div node-type="feed_list_forwardContent" ??>
                <div>
                    <div class="WB_info">??</div>
                    <div class="WB_text" node-type="feed_list_reason">??</div>
                    <div node-type="feed_list_media_prev">??</div>
                    <div class="WB_func clearfix">??</div>
                </div>
            </div>            
            '''
            forwards = {'forward_msg': '', 'forward_msgurl': '', 
                        'forward_msg_id': '', 'forward_media': '', 
                        'forward_msgtime': '', 'forward_msgfrom': '',
                        'forward_n_likes': '0', 'forward_n_forwards': '0',
                        'forward_n_favorites': '0', 'forward_n_comments': '0',
                        'forward_map_data': ''}
            
            info = _parse_forward_info(node.find('div div.WB_info'))
            msg  = _parse_msg(node.find('div div.WB_text'))
            if msg is not None:
                forwards['forward_msg']  = msg.strip().replace(',', u'，').replace(';', u'；')
                forwards['forward_media']= _parse_media(node.find('div[node-type="feed_list_media_prev"]'))
                forwards['forward_map_data']= _parse_map(node.find('div.map_data'))
                forwards['forward_msgurl'], forwards['forward_msgtime'], \
                    forwards['forward_msgfrom'] \
                        = _parse_from(node.find('div div.WB_func div.WB_from'))
                forwards['forward_n_likes'], forwards['forward_n_forwards'], \
                    forwards['forward_n_favorites'], forwards['forward_n_comments'] \
                        =_parse_handle(node.find('div div.WB_func div.WB_handle'))
                forwards['forward_msg_id'] = _parse_msg_id(node.find('div div.WB_func div.WB_handle'))
            else:
                forwards['forward_msg'] = u'抱歉，此微博已被作者删除。'
                
            forwards.update(info)
            
            return forwards
        
        def _parse_weibo(i):
            '''
            <div class="WB_detail">??</div>
            '''         
            node = pq(this)  # @UndefinedVariable
            
            weibo = dict.fromkeys(settings.WEIBO_KEY, '')
                        
            #---msg
            txt = _parse_msg(node.children('div[class="WB_text"][node-type="feed_list_content"]'))
            
            if txt is not None and (not txt.startswith(u'关注')):                
                weibo['msg'] = txt.strip().replace(',', u'，').replace(';', u'；')
                
                #---media
                weibo['media'] = _parse_media(node.children('ul[node-type="feed_list_media_prev"]'))
                
                #---msgurl, msgtime, msgfrom
                weibo['msgurl'], weibo['msgtime'], weibo['msgfrom'] = \
                    _parse_from(node.children('div.WB_func div.WB_from'))
                
                weibo['uid'] = weibo['msgurl'].split('http://weibo.com/')[-1].split('/')[0]
                try:
                    nickname = node.children('div.WB_func div.WB_handle a[action-type="feed_list_forward"]').attr('action-data')
                    weibo['nickname'] = nickname.split('&name=')[-1].split('&uid=')[0].strip()
                except:
                    pass
                
                #---number of like, forward, favorite, comment
                weibo['n_likes'], weibo['n_forwards'], \
                    weibo['n_favorites'], weibo['n_comments'] = \
                      _parse_handle(node.children('div.WB_func div.WB_handle'))
                
                #---mid
                weibo['msg_id'] = _parse_msg_id(node.children('div.WB_func div.WB_handle'))
                
                #---map data
                weibo['map_data'] = _parse_map(node.children('div.map_data'))
                
                #forward
                forward_node = node.children('div[node-type="feed_list_forwardContent"]')
                
                weibo['is_forward'] = False
                if len(forward_node) > 0:
                    weibo['is_forward'] = True
                    forward = _parse_forward(forward_node)
                    
                    weibo.update(forward)
                
                #storage
                self.storage.save_weibo(weibo)
                
        pq_doc.find('div.WB_detail').each(_parse_weibo)
        
        #--page count
        cnt = 1
        try:
            pg = pq_doc.find('div.W_pages span.list a.W_moredown')
            pg_info = pg.attr('action-data').split('&')
            cnt = int(pg_info[1].split('countPage=')[-1])
        except:
            pass
        
        return cnt

class ComFollowsParser(object):
    def __init__(self, storage):
        self.storage = storage
            
    def parse(self, pq_doc):
        def _parse_user(i):
            node = pq(this)  # @UndefinedVariable

            follow = dict.fromkeys(settings.USER_KEY, '')
            
            #--fetch time
            follow['fetch_time'] = str(time.time())[0:10]
            
            #---
            div_name   = pq(node.children('div.name'))
            #--
            div_name_a = div_name.children('a')
            for a in div_name_a:
                a = pq(a)
                try:
                    follow['uid'] = a.attr('usercard').split('=')[-1]
                    follow['nickname'] = a.text().strip()
                except AttributeError:
                    pass
                
                if a.attr('href').startswith('http://club.weibo.com/'):
                    follow['daren'] = a.children('i.W_ico16.ico_club').attr('title')
                elif a.attr('href').startswith('http://verified.weibo.com/'):
                    follow['verified'] = a.children('i.W_ico16').attr('title')
                elif a.attr('href').startswith('http://vip.weibo.com'):
                    follow['vip'] = a.attr('title')

            #--            
            addr = div_name.children('span.addr')
            
            follow['addr']= addr.text()
            
            sex  = addr.children('em').attr('class').split(' ')[-1]
            if sex.strip().lower() == 'female':
                follow['sex'] = u'女'
            elif sex.strip().lower() == 'male':
                follow['sex'] = u'男'
            #---
            connect_a = pq(node.children('div.connect a'))
            for a in connect_a:
                a = pq(a)
                if a.attr('href').endswith('follow'):
                    follow['n_follows'] = int(a.text().strip())
                elif a.attr('href').endswith('fans'):
                    follow['n_fans'] = int(a.text().strip())
                elif a.attr('href').startswith('/'):
                    follow['n_weibos'] = int(a.text().strip())
            
            #---
            info = pq(node.children('div.info'))
            try:
                follow['intro'] = info.text().strip().replace(',', u'，').replace(';', u'；')
            except AttributeError:
                pass
            
            #---
            follow_from = pq(node.children('div.from a'))
            follow['follow_from'] = follow_from.text()
            
            #storage
            self.storage.save_follow(follow)
                 
        query = 'ul[class="cnfList"][node-type="userListBox"] li div[class="con"] div[class="con_left"]'
        con_lefts = pq_doc.find(query)
        con_lefts.each(_parse_user)
        
        #--page count
        cnt = 1
        
        try:
            pg  = pq_doc.find('div[node-type="pageList"] a.page')[-1]
            cnt = int(pq(pg).attr('href').split('&page=')[-1].split('#')[0])
        except:
            pass
        
        return cnt
        
class ComFansParser(object):
    def __init__(self, storage):
        self.storage = storage
                        
    def parse(self, pq_doc):
        def _parse_user(i):
            node = pq(this)  # @UndefinedVariable
            
            fan = dict.fromkeys(settings.USER_KEY, '')
            
            #--fetch time
            fan['fetch_time'] = str(time.time())[0:10]
            
            #---
            div_name   = pq(node.children('div.name'))
            #--
            div_name_a = div_name.children('a')
            for a in div_name_a:
                a = pq(a)
                try:
                    fan['uid'] = a.attr('usercard').split('id=')[-1]
                    fan['nickname'] = a.text().strip()
                except AttributeError:
                    pass
                
                if a.attr('href').startswith('http://club.weibo.com/'):
                    fan['daren'] = a.children('i.W_ico16.ico_club').attr('title')
                elif a.attr('href').startswith('http://verified.weibo.com/'):
                    fan['verified'] = a.children('i.W_ico16').attr('title')
                elif a.attr('href').startswith('http://vip.weibo.com'):
                    fan['vip'] = a.attr('title')

            #--            
            addr = div_name.children('span.addr')
            
            fan['addr']= addr.text()
            
            sex  = addr.children('em').attr('class').split(' ')[-1]
            if sex.strip().lower() == 'female':
                fan['sex'] = u'女'
            elif sex.strip().lower() == 'male':
                fan['sex'] = u'男'

            #---
            connect_a = pq(node.children('div.connect a'))
            for a in connect_a:
                a = pq(a)
                if a.attr('href').endswith('follow'):
                    fan['n_follows'] = int(a.text().strip())
                elif a.attr('href').endswith('fans'):
                    fan['n_fans'] = int(a.text().strip())
                elif a.attr('href').startswith('/'):
                    fan['n_weibos'] = int(a.text().strip())
            
            #---
            info = pq(node.children('div.info'))
            try:
                fan['intro'] = info.text().strip().replace(',', u'，').replace(';', u'；')
            except AttributeError:
                fan['intro'] = ''
            
            #---
            follow_from  = pq(node.children('div.from a'))
            fan['follow_from'] = follow_from.text()
            
            #storage
            self.storage.save_fan(fan)   

        query = 'ul[class="cnfList"][node-type="userListBox"] li div[class="con"] div[class="con_left"]'
        con_lefts = pq_doc.find(query)
        con_lefts.each(_parse_user)
        
        #--page count
        cnt = 1
        
        try:
            pg  = pq_doc.find('div[node-type="pageList"] a.page')[-1]
            cnt = int(pq(pg).attr('href').split('&page=')[-1].split('#')[0])
        except:
            pass
           
        return cnt        

class ComInfosParser(object):
    def __init__(self, uid, storage):
        self.uid     = uid
        self.storage = storage
        
    def parse(self, pq_doc):
        profile = dict.fromkeys(settings.INFO_KEY, '')
        
        profile_map= {
            u'昵称': {'field': 'nickname'},
            u'所在地': {'field': 'location'},
            u'性别': {'field': 'sex'},
            u'生日': {'field': 'birth'},
            u'博客': {'field': 'blog'},
            u'个性域名': {'field': 'domain'},
            u'简介': {'field': 'intro'},
            u'邮箱': {'field': 'email'},
            u'QQ': {'field': 'QQ'},
            u'MSN': {'field': 'MSN'},
            u'大学': {'field': 'university'},
            u'公司': {'field': 'company'},
            u'标签': {'field': 'tag'}
        }
        
        profile['uid'] = self.uid
        #---
        connect = pq_doc.find('ul.user_atten li a strong')
        for a in connect:
            a = pq(a)
            if a.attr('node-type').lower() == 'follow':
                profile['n_follows'] = a.text().strip()
            elif a.attr('node-type').lower() == 'fans':
                profile['n_fans'] = a.text().strip()
            elif a.attr('node-type').lower() == 'weibo':
                profile['n_weibos'] = a.text().strip()
                
        #---
        pprofile = pq_doc.find('div.pf_item')
        for a in pprofile:
            a = pq(a)
            k = a.children('div.label').text().strip()
            v = a.children('div.con').text().strip()
            if k in profile_map:
                try:
                    v = v.replace(',', u'，').replace(';', u'；')
                    profile[profile_map[k]['field']] = v
                except AttributeError, e:
                    msg = 'In ComInfosParser.parse: parse %s: %s' %(profile_map[k]['field'], str(e))
                    print msg

        #---
        query = 'div.prm_app_pinfo div.info_block'
        pprofile_infoGrow = pq_doc.find(query)
        
        profile['daren_interests'] = ''
        profile['medal'] = ''   #勋章信息
        for infoblk in pprofile_infoGrow:
            infoblk = pq(infoblk)
            pinfo_title = infoblk.children('form.pinfo_title').text().strip()
            
            if u'达人信息' == pinfo_title:
                daren_info = infoblk.children('div.if_verified p.iv_vinfo a')
                try:
                    for a in daren_info:
                        a = pq(a)
                        if a.attr('href').endswith('&loc=daren'):
                            profile['daren_level'] = a.text().strip()
                        elif a.attr('href').endswith('&loc=darenscore'):
                            profile['daren_score'] = a.text().strip()
                        elif a.attr('href').endswith('&loc=darenint'):
                            profile['daren_interests'] += '-' + a.text().strip()
                    
                    profile['daren_interests'] = profile['daren_interests'].strip()
                except Exception, e:
                    msg = 'In ComInfosParser.parse: parse daren-%s' %str(e)
                    print msg
            elif u'勋章信息' == pinfo_title:
                bagdelist = infoblk.children('div.if_badge[node-type="medal"] ul.bagde_list li a')
                for b in bagdelist:
                    b = pq(b)
                    profile['medal'] += b.attr('title').strip() + '+'
                profile['medal'].strip()
            elif u'等级信息' == pinfo_title:
                level = infoblk.children('div.if_level p.level_info span.info')
                for l in level:
                    l = pq(l)
                    try:
                        t = l.text().strip().split(u'：')
                        if u'当前等级' == t[0].strip():
                            profile['cur_level'] = t[1].strip()
                        elif u'活跃天数' == t[0].strip():
                            profile['active_days'] = t[1].strip()
                        elif u'距离下一级别' == t[0].strip():
                            profile['next_level_days'] = t[1].strip()
                    except Exception, e:
                        msg = 'In ComInfosParser.parse: parse level-%s' %str(e)
                        print msg
            elif u'信用信息' == pinfo_title:
                trust = infoblk.children('div.if_trust div div.trust_info span.info')
                for t in trust:
                    t = pq(t)
                    try:
                        v = t.text().strip().split(u'：')
                        if u'信用等级' == v[0].strip():
                            profile['trust_level'] = v[1].strip()
                        elif u'当前信用积分' == v[0].strip():
                            profile['trust_score'] = v[1].strip()
                    except Exception, e:
                        msg = 'In ComInfosParser.parse: parse trust level-%s' %str(e)
                        print msg
        #storage
        self.storage.save_info(profile)        

class ComRepostsParser(object):
    strptime_lock = Lock() # added lock for datetime.strptime method is not thread-safe.
    
    def __init__(self, msg_id, storage):
        self.msg_id  = msg_id
        self.storage = storage
        
    def _strptime(self, string, format_):
        self.strptime_lock.acquire()
        try:
            return datetime.datetime.strptime(string, format_)
        finally:
            self.strptime_lock.release()
        
    def parse_datetime(self, dt_str):
        dt = None
        if u'秒' in dt_str:
            sec = int(dt_str.split(u'秒', 1)[0].strip())
            dt = datetime.datetime.now() - datetime.timedelta(seconds=sec)
        elif u'分钟' in dt_str:
            sec = int(dt_str.split(u'分钟', 1)[0].strip()) * 60
            dt = datetime.datetime.now() - datetime.timedelta(seconds=sec)
        elif u'今天' in dt_str:
            dt_str = dt_str.replace(u'今天', datetime.datetime.now().strftime('%Y-%m-%d'))
            dt = self._strptime(dt_str, '%Y-%m-%d %H:%M')
        elif u'月' in dt_str and u'日' in dt_str:
            this_year = datetime.datetime.now().year
            dt = self._strptime('%s %s' % (this_year, dt_str), '%Y %m月%d日 %H:%M')
        else:
            dt = self._strptime(dt_str, '%Y-%m-%d %H:%M')
            
        return time.mktime(dt.timetuple())
    
    def parse(self, pq_doc):
        def _parse(i):
            '''
            <dd>
                <a title="" href="">nickname</a>：text/imag
                <span class="S_txt2">time</span>
                <div class="info">
                    ...
                    <a action-type="replycomment" href="" 
                        action-data="ouid=*&*&status_owner_user=*">??</a>
                </div>
            </dd>
            '''
            
            node = pq(this)  # @UndefinedVariable
            
            info = dict.fromkeys(settings.REPOST_KEY, '')
            
            #--retweet user info
            user_info = node.children('a')
            
            for a in user_info:
                a = pq(a)
                                  
                if a.attr('href').startswith('http://club.weibo.com/'):
                    info['daren'] = a.children('i.W_ico16.ico_club').attr('title')
                elif a.attr('href').startswith('http://verified.weibo.com/'):
                    info['verified'] = a.children('i.W_ico16').attr('title')
                elif a.attr('href').startswith('http://vip.weibo.com'):
                    info['vip'] = a.attr('title')     
            
            #--time
            try:
                t = node.children('div.info span.fl').text().split('|')[0]
                info['msg_time'] = str(self.parse_datetime(t.strip()))[0:10]
            except Exception, e:
                msg = 'In ComRepostsParser.parse: parse time-%s' %str(e)
                print msg
                info['msg_time'] = None
                
            #--contents
            content = node.children('em').text()
            info['msg'] = content
            
            #---root user info
            a = node.children('div.info a[action-type="feed_list_forward"]')
            data = a.attr('action-data').split('&')
            
            for d in data:
                if d.startswith('rootmid'):
                    info['forward_msg_id'] = d.split('rootmid=')[-1]
                elif d.startswith('rootname'):
                    info['forward_nickname'] = d.split('rootname=')[-1]
                elif d.startswith('rootuid'):
                    info['forward_uid'] = d.split('rootuid=')[-1]
                elif d.startswith('rooturl'):
                    info['forward_msg_url'] = d.split('rooturl=')[-1]
                elif d.startswith('url'):
                    info['msg_url'] = d.split('url=')[-1]
                elif d.startswith('mid'):
                    info['msg_id'] = d.split('mid=')[-1]
                elif d.startswith('name='):
                    info['nickname'] = d.split('name=')[-1]
                elif d.startswith('uid'):
                    info['uid'] = d.split('uid=')[-1]
                        
            self.storage.save_msg_repost(info)
            
        pq_doc.find('dl.comment_list dd').each(_parse)

class ComCommentsParser(object):
    strptime_lock = Lock() # added lock for datetime.strptime method is not thread-safe.
    
    def __init__(self, msg_id, storage):
        self.msg_id  = msg_id
        self.storage = storage
        
    def _strptime(self, string, format_):
        self.strptime_lock.acquire()
        try:
            return datetime.datetime.strptime(string, format_)
        finally:
            self.strptime_lock.release()
        
    def parse_datetime(self, dt_str):
        dt = None
        if u'秒' in dt_str:
            sec = int(dt_str.split(u'秒', 1)[0].strip())
            dt = datetime.datetime.now() - datetime.timedelta(seconds=sec)
        elif u'分钟' in dt_str:
            sec = int(dt_str.split(u'分钟', 1)[0].strip()) * 60
            dt = datetime.datetime.now() - datetime.timedelta(seconds=sec)
        elif u'今天' in dt_str:
            dt_str = dt_str.replace(u'今天', datetime.datetime.now().strftime('%Y-%m-%d'))
            dt = self._strptime(dt_str, '%Y-%m-%d %H:%M')
        elif u'月' in dt_str and u'日' in dt_str:
            this_year = datetime.datetime.now().year
            dt = self._strptime('%s %s' % (this_year, dt_str), '%Y %m月%d日 %H:%M')
        else:
            dt = self._strptime(dt_str, '%Y-%m-%d %H:%M')
            
        return time.mktime(dt.timetuple())
    
    def parse(self, pq_doc):
        def _parse(i):
            '''
            <dd>
                <a title="" href="">nickname</a>：text/imag
                <span class="S_txt2">time</span>
                <div class="info">
                    ...
                    <a action-type="replycomment" href="" 
                        action-data="ouid=*&*&status_owner_user=*">??</a>
                </div>
            </dd>
            '''
            
            node = pq(this)  # @UndefinedVariable
            
            info = dict.fromkeys(settings.COMMENT_KEY, '')
                        
            #--retweet user info
            user_info = node.children('a')
                        
            for a in user_info:
                a = pq(a)
                
                try:
                    if a.attr('usercard').startswith('id=') and a.attr('href').startswith('/'):
                        info['nickname'] = a.attr('title')
                except Exception, e:
                    msg = 'In ComCommentsParser.parse: parse uid+nickname-%s' %str(e)
                    print msg
                
                if a.attr('href').startswith('http://club.weibo.com/'):
                    info['daren'] = a.children('i.W_ico16.ico_club').attr('title')
                elif a.attr('href').startswith('http://verified.weibo.com/'):
                    info['verified'] = a.children('i.W_ico16').attr('title')
                elif a.attr('href').startswith('http://vip.weibo.com'):
                    info['vip'] = a.attr('title')     
            
            #--time
            t = node.children('span').text()
            info['msg_time'] = str(self.parse_datetime(t.strip('()')))[0:10]
            
            #--contents
            content = node.text().split(t)[0].strip().replace(',', u'，').replace(';', u'；')
            content = content.split(info['nickname'] + u' ：')[-1]
            
            info['msg'] = content
            
            #---root user info
            a = node.children('div.info a[action-type="replycomment"]')
            data = a.attr('action-data').split('&')
            
            for d in data:
                if d.startswith('ouid'):
                    info['uid'] = d.split('ouid=')[-1]
                elif d.startswith('cid'):
                    info['msg_id'] = d.split('cid=')[-1]
                elif d.startswith('mid'):
                    info['forward_msg_id'] = d.split('mid=')[-1]
                elif d.startswith('content'):
                    info['nickname'] = d.split('content=')[-1]
                elif d.startswith('status_owner_user'):
                    info['forward_uid'] = d.split('status_owner_user=')[-1]
            
            self.storage.save_msg_comment(info)
            
        pq_doc.find('dl.comment_list dd').each(_parse)        

class CnWeibosParser(object):
    def __init__(self, uid, storage):
        self.uid = uid
        self.storage = storage
        
    def parse(self, pq_doc):
        raise ValueError('Please use ComWeiboParser')

class CnFollowsParser(object):
    def __init__(self, uid, storage):
        self.uid = uid
        self.storage = storage
        
    def parse(self, pq_doc):
        def _parse_user(i):
            
            node = pq(this)  # @UndefinedVariable
            
            follow = dict.fromkeys(settings.USER_KEY, '')
            
            #--fetch time
            follow['fetch_time'] = str(time.time())[0:10]
            
            links = node.children('a')
            
            follow['nickname'] = pq(links[0]).text()
            follow['uid'] = pq(links[-1]).attr('href').split('?')[-1].split('&')[0].split('uid=')[-1]

            self.storage.save_follow(follow)
            
        #--
        pq_doc.find('table tr td:last-child').each(_parse_user)
        
        #--page count
        cnt = 1
        try:
            pg = pq_doc.find('div#pagelist.pa form div input[name="mp"]')
            cnt= int(pg.attr('value'))
        except Exception, e:
            msg = 'In CnFollowsParser.parse: parse page count: %s' %str(e)
            print msg
        
        return cnt

class CnFansParser(object):
    def __init__(self, uid, storage):
        self.uid = uid
        self.storage = storage
        
    def parse(self, pq_doc):
        def _parse_user(i):
            node = pq(this)  # @UndefinedVariable
            
            fan = dict.fromkeys(settings.USER_KEY, '')
            
            #--fetch time
            fan['fetch_time'] = str(time.time())[0:10]
            
            links = node.children('a')
            
            fan['nickname'] = pq(links[0]).text()
            fan['uid'] = pq(links[-1]).attr('href').split('?')[-1].split('&')[0].split('uid=')[-1]

            self.storage.save_fan(fan)
            
        #--
        pq_doc.find('table tr td:last-child').each(_parse_user)
        
        #--page count
        cnt = 1
        try:
            pg = pq_doc.find('div#pagelist.pa form div input[name="mp"]')
            cnt= int(pg.attr('value'))
        except Exception, e:
            msg = 'In CnFansParser.parse: parse page count: %s' %str(e)
            print msg
        
        return cnt

class CnInfosParser(object):
    def __init__(self, uid, storage):
        self.uid = uid
        self.storage = storage
        
    def parse(self, pq_doc):
        raise ValueError('Please use ComInfoParser')