# encoding: utf-8
COMWEIBO_COOKIE = 'weibo.com.cookie.dat'
CNWEIBO_COOKIE  = 'weibo.cn.cookie.dat'

PAGE_LIMIT = 10

QUERY_WEIBOS = (('<script>STK && STK.pageletM && STK.pageletM.view({"pid":'
                 '"pl_content_weiboDetail"'), \
                ('<script>FM.view({"ns":"pl.content.weiboDetail.index","domid":'
                 '"Pl_Official_LeftWeiboDetail__28"'))

QUERY_WEIBOS_MID = ('div.WB_detail div[node-type="feed_list"]')

QUERY_FOLLOWS = (('<script>STK && STK.pageletM && STK.pageletM.view({"pid":'
                    '"pl_relation_hisFollow"'), \
                 ('<script>FM.view({"ns":"pl.content.followTab.index","domid":'
                  '"Pl_Official_LeftHisRelation__15"'), \
                 ('<script>FM.view({"ns":"pl.content.followTab.index","domid":'
                  '"Pl_Official_LeftHisRelation__21"'), \
                 ('<script>FM.view({"ns":"pl.content.followTab.index","domid":'
                  '"Pl_Official_LeftHisRelation__16"'))

QUERY_FANS    = (('<script>STK && STK.pageletM && STK.pageletM.view({"pid":'
                    '"pl_relation_hisFans"'), \
                 ('<script>FM.view({"ns":"pl.content.followTab.index","domid":'
                  '"Pl_Official_LeftHisRelation__15"'), \
                 ('<script>FM.view({"ns":"pl.content.followTab.index","domid":'
                  '"Pl_Official_LeftHisRelation__21"'), \
                 ('<script>FM.view({"ns":"pl.content.followTab.index","domid":'
                  '"Pl_Official_LeftHisRelation__16"'))

QUERY_INFO    = (('<script>STK && STK.pageletM && STK.pageletM.view({"pid":'
                    '"pl_profile_photo"'), \
                 ('<script>FM.view({"ns":"pl.header.head.index","domid":'
                  '"Pl_Official_Header__1"'), \
                 ('<script>STK && STK.pageletM && STK.pageletM.view({"pid":'
                 '"pl_profile_infoBase"'),  \
                 ('<script>FM.view({"ns":"","domid":"Pl_Official_LeftInfo__13"'), \
                 ('<script>STK && STK.pageletM && STK.pageletM.view({"pid":'
                  '"pl_profile_infoCareer"'),\
                 ('<script>STK && STK.pageletM && STK.pageletM.view({"pid":'
                  '"pl_profile_infoEdu"'),   \
                 ('<script>STK && STK.pageletM && STK.pageletM.view({"pid":'
                  '"pl_profile_infoTag"'),   \
                 ('<script>STK && STK.pageletM && STK.pageletM.view({"pid":'
                  '"pl_profile_infoGrow"'), \
                 ('<script>FM.view({"ns":"","domid":"Pl_Official_RightGrow__14"'),\
                 ('<script>FM.view({"ns":"","domid":"Pl_Official_LeftInfo__14"'), \
                 ('<script>FM.view({"ns":"","domid":"Pl_Official_RightGrow__15"'))

MASK_WEIBO  = 0b100000
MASK_FOLLOW = 0b010000
MASK_FAN    = 0b001000
MASK_INFO   = 0b000100
MASK_REPOST = 0b000010
MASK_COMMENT= 0b000001

SUFFIX_WEIBOS_F  = '-weibos-'
SUFFIX_FOLLOWS_F = '-follows-'
SUFFIX_FANS_F    = '-fans-'
SUFFIX_INFOS_F   = '-infos-'
SUFFIX_REPOSTS_F = '-reposts-'
SUFFIX_COMMENTS_F= '-comments-'

WEIBO_KEY = [
    'uid', 'nickname', 'msg', 'msgurl', 'msg_id', 'msgtime', 'msgfrom', 'media', 
    'map_data', 'n_likes', 'n_forwards', 'n_favorites', 'n_comments', 'is_forward',
    'forward_uid', 'forward_nickname', 'forward_daren', 'forward_verified', 
    'forward_vip', 'forward_msg', 'forward_msgurl', 'forward_msg_id', 
    'forward_msgtime', 'forward_msgfrom', 'forward_media', 'forward_map_data',
    'forward_n_likes', 'forward_n_forwards', 'forward_n_favorites', 
    'forward_n_comments'
]

USER_KEY = [
    'uid', 'nickname', 'sex', 'addr', 'daren', 'verified', 'vip', 'n_follows', 
    'n_fans', 'n_weibos', 'intro', 'follow_from', 'fetch_time'
]

INFO_KEY = [
    'uid', 'nickname', 'location', 'sex', 'birth', 'blog', 'domain', 'intro', 
    'email', 'QQ', 'MSN', 'university', 'company', 'tag', 'n_follows', 
    'n_fans', 'n_weibos', 'daren_level', 'daren_score', 'daren_interests', 
    'medal', 'cur_level', 'active_days', 'next_level_days',
    'trust_level', 'trust_score'
]

REPOST_KEY = [
    'uid', 'nickname', 'daren', 'verified', 'vip', 
    'msg', 'msg_url', 'msg_id', 'msg_time', 
    'forward_uid', 'forward_nickname', 'forward_msg_url', 'forward_msg_id'     
]

COMMENT_KEY = [
    'uid', 'nickname', 'daren', 'verified', 'vip', 
    'msg', 'msg_url', 'msg_id', 'msg_time', 
    'forward_uid', 'forward_nickname', 'forward_msg_url', 'forward_msg_id'     
]
