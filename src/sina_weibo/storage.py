# encoding: utf-8

import codecs
import csv
import os
import settings
import time

class Storage(object):
    def __init__(self, _id):
        self.id = _id
                
    def save_weibo(self, weibo):
        raise NotImplementedError
        
    def save_weibos(self, weibos):
        raise NotImplementedError

    def save_follow(self, user):
        raise NotImplementedError

    def save_follows(self, users):
        raise NotImplementedError

    def save_fan(self, user):
        raise NotImplementedError
    
    def save_fans(self, users):
        raise NotImplementedError

    def save_info(self, info):
        raise NotImplementedError
    
    def save_msg_repost(self, repost):
        raise NotImplementedError
    
    def save_msg_reposts(self, reposts):
        raise NotImplementedError
    
    def save_msg_comment(self, comment):
        raise NotImplementedError
    
    def save_msg_comments(self, comments):
        raise NotImplementedError
    
class FileStorage(Storage):
    def __init__(self, _id, data_type, folder='./'):
        Storage.__init__(self, _id=_id)
        
        t = time.strftime('%Y-%m-%d-%H-%M', time.localtime())
        
        if data_type & settings.MASK_WEIBO == settings.MASK_WEIBO:
            name = str(_id) + settings.SUFFIX_WEIBOS_F + t + '.csv'
            self.weibos_f_name = os.path.join(folder, name)
            self.weibos_fp     = codecs.open(self.weibos_f_name, 'w+', 'utf-8')
            self.weibos_wr     = csv.DictWriter(self.weibos_fp, delimiter='\t',
                                                fieldnames=settings.WEIBO_KEY)
            
            self.weibos_wr.writeheader()
            
        if data_type & settings.MASK_FOLLOW == settings.MASK_FOLLOW:
            name = str(_id) + settings.SUFFIX_FOLLOWS_F + t + '.csv'
            self.follows_f_name = os.path.join(folder, name)
            self.follows_fp     = codecs.open(self.follows_f_name, 'w+', 'utf-8')
            self.follows_wr     = csv.DictWriter(self.follows_fp, delimiter='\t',
                                                 fieldnames=settings.USER_KEY)
            
            self.follows_wr.writeheader()
            
        if data_type & settings.MASK_FAN == settings.MASK_FAN:
            name = str(_id) + settings.SUFFIX_FANS_F + t + '.csv'
            self.fans_f_name = os.path.join(folder, name)
            self.fans_fp     = codecs.open(self.fans_f_name, 'w+', 'utf-8')
            self.fans_wr     = csv.DictWriter(self.fans_fp, delimiter='\t',
                                              fieldnames=settings.USER_KEY)
            
            self.fans_wr.writeheader()
            
        if data_type & settings.MASK_INFO == settings.MASK_INFO:
            name = str(_id) + settings.SUFFIX_INFOS_F + t + '.csv'
            self.infos_f_name = os.path.join(folder, name)
            self.infos_fp     = codecs.open(self.infos_f_name, 'w+', 'utf-8')
            self.infos_wr     = csv.DictWriter(self.infos_fp, delimiter='\t',
                                               fieldnames=settings.INFO_KEY)
            
            self.infos_wr.writeheader()
            
        if data_type & settings.MASK_REPOST == settings.MASK_REPOST:
            name = str(_id) + settings.SUFFIX_REPOSTS_F + t + '.csv'
            self.reposts_f_name = os.path.join(folder, name)
            self.reposts_fp     = codecs.open(self.reposts_f_name, 'w+', 'utf-8')
            self.reposts_wr     = csv.DictWriter(self.reposts_fp, delimiter='\t',
                                                 fieldnames=settings.REPOST_KEY)
            
            self.reposts_wr.writeheader()
            
        if data_type & settings.MASK_COMMENT == settings.MASK_COMMENT:
            name = str(_id) + settings.SUFFIX_COMMENTS_F + t + '.csv'
            self.comments_f_name = os.path.join(folder, name)
            self.comments_fp     = codecs.open(self.comments_f_name, 'w+', 'utf-8')
            self.comments_wr     = csv.DictWriter(self.comments_fp, delimiter='\t',
                                                  fieldnames=settings.COMMENT_KEY)
            
            self.comments_wr.writeheader()
            
    def delete(self, fp, f_name):
        if os.path.exists(f_name):
            try:
                fp.close()
                os.remove(f_name)
            except:
                pass
            
    def save_weibo(self, weibo):
        self.weibos_wr.writerow(weibo)
        
    def save_weibos(self, weibos):
        self.weibos_wr.writerows(weibos)

    def save_follow(self, user):
        self.follows_wr.writerow(user)

    def save_follows(self, users):
        self.follows_wr.writerows(users)

    def save_fan(self, user):
        self.fans_wr.writerow(user)
    
    def save_fans(self, users):
        self.fans_wr.writerows(users)

    def save_info(self, info):
        self.infos_wr.writerow(info)
    
    def save_msg_repost(self, repost):
        self.reposts_wr.writerow(repost)
    
    def save_msg_reposts(self, reposts):
        self.reposts_wr.writerows(reposts)
    
    def save_msg_comment(self, comment):
        self.comments_wr.writerow(comment)
    
    def save_msg_comments(self, comments):
        self.comments_wr.writerows(comments)