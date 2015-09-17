#!/usr/bin/python
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html", title="Proton Pack")

application = tornado.web.Application([
	(r"/", MainHandler),
])

if __name__ == "__main__":
	application.listen(80)
	tornado.ioloop.IOLoop.current().start()
