from handlers import routines
import settings
import tornado.ioloop
import tornado.web

sets = {
	'debug': settings.DEBUG,
	'static_path': settings.STATIC_PATH,
	'cookie_secret': '24oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
	'xsrf_cookies': True,
}

application = tornado.web.Application(routines, **sets)

def main():
	application.listen(settings.PAGE_PORT)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()