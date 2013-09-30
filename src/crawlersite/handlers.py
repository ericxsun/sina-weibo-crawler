# coding: utf-8

from tornado.web import RequestHandler, asynchronous

class BaseHandler(RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie('user')

	def check_user(self):
		if not self.current_user:
			self.redirect('/')
			return

class LoginHandler(BaseHandler):
	@asynchronous
	def post(self):
		if not self.request.headers.get('Cookie'):
			self.write('The Browser does not support Cookie')

		uri = self.request.body

		post_data = {}
		for i in url.split('&'):
			data = i.split('=')

			if data[0] == 'login':
				data[1] = urllib2.unquote(urllib2.unquote(urllib2.unquote(data[1])))

			post_data[data[0]] = data[1]

		db = SqlHandler()
		for i in ['account', 'password']:
			flag = getattr(db, i)(post_data[i])

			if not flag:
				self.write('Error: %s' %i)

				return

		self.set_secure_cookie('user', post_data['account'])
		self.render('templates/userres.html', post_data['account'])

class LogoutHandler(RequestHandler):
	@asynchronous
	def get(self):
		self.clear_cookie('user')
		self.redirect('/')

class RootHandler(RequestHandler):
	@asynchronous
	def get(self):
		kwargs = {}
		self.render('templates/index.html', **kwargs)

class ToolsResHandler(BaseHandler):
	@asynchronous
	def get(self):
		self.render('templates/tools.html')

class UserResHandler(BaseHandler):
	@asynchronous
	def get(self):
		self.render('templates/userres.html')

class PublicResHandler(BaseHandler):
	@asynchronous
	def get(self):
		self.render('templates/publicres.html')

class WeiboResHandler(BaseHandler):
	@asynchronous
	def get(self):
		self.render('templates/weibores.html')

class ProfileResHandler(BaseHandler):
	@asynchronous
	def get(self):
		self.render('templates/profileres.html')

class RelationResHandler(BaseHandler):
	@asynchronous
	def get(self):
		self.render('templates/relationres.html')

class FAQHandler(BaseHandler):
	@asynchronous
	def get(self):
		self.render('templates/faq.html')

class AboutHandler(BaseHandler):
	@asynchronous
	def get(self):
		self.render('templates/about.html')


routines = [
	(r'/', RootHandler),
	(r'/login', LoginHandler),
	(r'/logout', LogoutHandler),
	(r'/tools', ToolsResHandler),
	(r'/userres', UserResHandler),
	(r'/publicres', PublicResHandler),
	(r'/weibores', WeiboResHandler),
	(r'/profileres', ProfileResHandler),
	(r'/relationres', RelationResHandler),
	(r'/faq', FAQHandler),
	(r'/about', AboutHandler)
]
