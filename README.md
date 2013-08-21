sina-weibo-crawler
==================

本项目实为实验室微博数据分析中的数据采集模块(针对<a href='http://weibo.com'>新浪微博</a>), 可以采集指定用户的微博, 关注, 粉丝, 也可以采集指定消息的转发和评论. 网络上已经出现了很多的微博crawler, 如<a href='http://114.113.145.13/'>中国爬盟</a>, <a href='http://qinxuye.me/article/cola-a-distributed-crawler-framework/'>Cola：一个分布式爬虫框架</a>. 再次发明了轮子, 囧, 记得帮主说过一句话:还是自家的好,我就心宽了, 哈哈.

注: 其中的登录和cookie管理均来自<a href='http://114.113.145.13/'>中国爬盟</a>, 非常感谢.


snapshot
========

![snapshot of login](https://raw.github.com/followyourheart/sina-weibo-crawler/master/login.jpg)

![snapshot of crawl](https://raw.github.com/followyourheart/sina-weibo-crawler/master/crawl.jpg)


requirements
============

1) python2.7

2) wxPython
<p>$yum install wxPython</p>

3) rsa
<p>$easy_install rsa</p>

4) lxml
<p>$easy_install lxml</p>

if any error occur
<p>$yum install python-lxml</p>

5) pyquery
<p>$easy_install pyquery</p>

EXE
===
using <a href='http://www.pyinstaller.org/'>Pyinstaller</a> converts this project into stand-alone executables

for example:
<p>$python pyinstall.py --onefile $crawler_dir/unix_local_login.py</p>
<p>>python pyinstall.py --Fw $crawler_dir/win_local_login.py</p>

TODO
====


keys and the meaning resepectively
==================================

WEIBO
-----


| key 					      | meaning 							                  		| example 						          			            	|
| ------------------- | ------------------------------------------- | ------------------------------------------------- |
| uid 			      		| 用户ID(数字) 								                | 1000000253 						              	        		|
| nickname 		    		| 用户昵称 	                  								| 茶歇时间 						                      				|
| msg 	      				| 消息内容 						                  			| 一公司网管：老板知道装了360上不了QQ，高兴坏了... 	|
| msgurl 		      		| 消息URL 						                  			| http://weibo.com/1000000253/zF0sMQjYKS 		        |
| msg_id 		      		| 消息ID(数字) 								                | 3471354253 							                      		|
| msgtime 		    		| 消息发布时间(linux时间戳) 				        	| 1289012596 	                      								|
| msgfrom 			     	| 消息来自(设备) 						              		| iPhone客户端 			                    						|
| media 		      		| 是否含有图片/音频/视频(True/False) 		    	| True 									                        		|
| map_data 			    	| 地图信息 						                  			|  				                          								|
| n_likes 				    | 赞 						                      				| 1 						                          					|
| n_forwards 		    	| 转发 						                     				| 1 					                          						|
| n_favorites 		  	| 收藏 							                    			| 1 						                          					|
| n_comments 		    	| 评论 								                    		| 1 								                          			|
| is_forward 			    | 本消息是否转发(True/) 						          | True 			                        								|
| forward_uid 		  	| 原始消息发布用者的ID(数字) 					        | 1644572034 					                      				|
| forward_nickname 		| 原始消息发布用者的昵称 					          	| 精彩语录 								                      		|
| forward_daren 		  | 原始消息发布用者的认证信息-达人 			    	| 微博达人 							                      			|
| forward_verified 		| 原始消息发布用者的认证信息-新浪认证 	      | 新浪认证 				                      						|
| forward_vip 			  | 原始消息发布用者的认证信息-新浪会员         | 微博会员 				                      						|
| forward_msg 			  | 原始消息 							            	      	|  											                          	|
| forward_msgurl 		  | 原始消息地址 							                	|  								                          				|
| forward_msg_id 		  | 原始消息ID(数字) 			              				|  												                          |
| forward_msgtime 		| 原始消息发布时间(linux时间戳) 		      		|  				                          								|
| forward_msgfrom 		| 原始消息来自(设备) 		            					|  				                          								|
| forward_media 		  | 原始消息是否含有图片/音频/视频(True/False) 	|  								                          				|
| forward_map_data 		| 原始消息地图信息 					              		|  								                          				|
| forward_n_likes 		| 原始消息赞 								                	|  												                          |
| forward_n_forwards 	| 原始消息转发 						                		|  										                          		|
| forward_n_favorites	| 原始消息收藏 								                |  								                          				|
| forward_n_comments 	| 原始消息评论 				                 				|  												                          |


USER-fans/follows
-----------------

| key 		    	| meaning     		| example 	|
| ------------- | --------------- | --------- |
| uid 		    	| 用户ID(数字) 	  |  		    	|
| nickname 	  	| 昵称 			      |  	    		|
| sex 			    | 性别    			  |   		  	|
| addr 	    		| 地址 	    		  |  		    	|
| daren 	    	| 达人 		    	  |  		    	|
| verified 	  	| 新浪认证 		    |  		    	|
| vip 			    | 新浪会员 	    	|  		    	|
| n_follows   	| 关注数 	      	|  		    	|
| n_fans 	    	| 粉丝数      		|  		    	|
| n_weibos 	  	| 微博数       		|  			    |
| intro 		    | 简介 		      	|  		    	|
| follow_from 	| 关注来自(设备) 	|  			    |


INFO-用户信息
-------------

| key 			    	| meaning 	    	| example 	|
| --------------- | --------------- | --------- |
| uid 			    	| 用户ID      		|  		    	|
| nickname  			| 昵称 			      |  		    	|
| location  			| 地址 		      	|  	    		|
| sex     				| 性别 	      		|  	    		|
| birth 		    	| 生日 			      |  	    		|
| blog 		    		| 博客 		      	|  		    	|
| domain    			| 个性域名 		    |  		    	|
| intro 	    		| 简介 		      	|  		    	|
| email      			| email 		      |  	    		|
| QQ 			      	| QQ        			|  		    	|
| MSN 				    | MSN 		      	|  	    		|
| university 		  | 教育 	       		|  		    	|
| company 			  | 工作 			      |  	    		|
| tag				      | 标签 		      	|  	    		|
| n_follows 		  | 关注数 	      	|  	    		|
| n_fans 			    | 粉丝数 		      |  	    		|
| n_weibos 			  | 微博数 	      	|  	    		|
| daren_level 		| 达人信息(等级) 	| 高级达人 	|
| daren_score 		| 达人信息(积分) 	|  		    	|
| daren_interests | 达人信息(爱好) 	|  	    		|
| medal 			    | 勋章信息 		    |  	    		|
| cur_level 		  | 当前等级 	    	|  	    		|
| active_days 		| 活跃天数 		    |  	    		|
| next_level_days | 距离下一级别 	  |     			|
| trust_level 		| 信用等级 		    |  		    	|
| trust_score 		| 当前信用积分 	  |     			|


REPOSTS/COMMENTS--消息转发/评论
-------------------------------

| key 				      | meaning 					            		    | example 	              								|
| ----------------- | ------------------------------------- | --------------------------------------- |
| uid 				      | 转发/评论消息用户的ID 			    	    |  				                  							|
| nickname 			    | 转发/评论消息用户的昵称 				      |  			                  								|
| daren 			      | 转发/评论消息用户的认证信息-达人 		  |  								                  			|
| verified 			    | 转发/评论消息用户的认证信息-新浪认证  |  							                  				|
| vip 				      | 转发/评论消息用户的认证信息-新浪会员 	|  								                  			|
| msg 				      | 转发/评论消息 			            			|  											                  |
| msg_url 			    | 转发/评论消息URL 					            |  										                  	|
| msg_id 			      | 转发/评论消息ID 				            	|  									                  		|
| msg_time 			    | 转发/评论时间(linuxlinux时间戳) 		  |  									                  		|
| forward_uid 		  | 原消息用户ID 						              |  											                  |
| forward_nickname 	| 原消息用户昵称 						            |  										                  	|
| forward_msg_url 	| 原消息URL 							              | http://weibo.com/1000000253/zF0sMQjYKS 	|
| forward_msg_id 	  | 原消息ID(数字) 						            | 3471354253 	              							|
