# encoding: utf-8

HOST = ''
PORT = 8000

SINA_WEIBO = 'SinaWeibo'
TWITTER    = 'Twitter'
FACEBOOK   = 'Facebook'

SITE_CHOICES = [SINA_WEIBO, TWITTER, FACEBOOK]
DATA_CHOICES = ['weibos', 'follows', 'fans', 'infos']

HOME_PAGE = 'http://www.cns.edu.cn'

DEVELOPERS = ['x.s.<followyourheart1211@gmail.com>']
LICENCE    = 'See %s' % HOME_PAGE
COPYRIGHT  = '(C) 2013 Center of Networked Systems'

LOCAL_VERSION = '1.0.0'
DISTR_VERSION = '1.0.0'

#localled_version_login
LOCAL_LOGIN_WIN_TITLE  = 'Using Weibo Account To Login'
LOCAL_LOGIN_WIN_STATUS = 'Version: %s' %LOCAL_VERSION

#local version crawler
LOCAL_CRAWLER_WIN_TITLE  = 'Local Version of Data Crawler'
LOCAL_CRAWLER_WIN_STATUS = 'All Copyright Reserved. CNS'

LOCAL_CRAWLER_HELP_TITLE = 'About the Crawler Client'
LOCAL_CRAWLER_HELP_DOC   = ('1. Nick Name: "search and crawl". That is: input'
                            ' the Nick Name, search and then start crawling;\n\n')
LOCAL_CRAWLER_HELP_DOC  += ('2. Multi User ID: "crawl the data of users". '
                            'That is: input some user IDs in digital format, '
                            'every two IDs with a semicolon as the delimiter, '
                            'and then start crawling;\n\n')
LOCAL_CRAWLER_HELP_DOC  += ('3. Message URL: "crawl the reposts and comments of '
                            'messages".  That is : input the url of messages, '
                            '(like: http://weibo.com/1000000253/ezC36cq3i6G), ' 
                            'every two URLs with a semicolon as the delimiter, '
                            'and then start crawling;\n\n')
LOCAL_CRAWLER_HELP_DOC  += ('4. For more information and data sets,'
                            ' please visit the Home Page of CNS.')

#distributed version login
DISTR_LOGIN_WIN_TITLE  = 'Using Site Account To Login'
DISTR_LOGIN_WIN_STATUS = 'Version: %s' %DISTR_VERSION

#distributed version crawler
DISTR_CRAWLER_WIN_TITLE  = 'Distributed Version of Data Crawler'
DISTR_CRAWLER_WIN_STATUS = 'All Copyright Reserved. CNS'

DISTR_CRAWLER_HELP_TITLE = 'About the Crawler Client'
DISTR_CRAWLER_HELP_DOC   = ('1. Use the account of weibo.com,'
                            ' twitter.com etc. to start the crawler;\n\n')
DISTR_CRAWLER_HELP_DOC  += ('2. For more information and data sets,'
                            ' please visit:')    