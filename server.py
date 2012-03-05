# Copyright (c) 2012, Dylan Hackers.
# See License.txt for details.

import tornado.ioloop
import tornado.web
import os
from opendylan.tornado.handlers import DylanBuildHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/build", DylanBuildHandler),
    (r"/static", tornado.web.StaticFileHandler, dict(path=settings['static_path']))
], **settings)

if __name__ == "__main__":
    print "Listening..."
    application.listen(8888)
    print "Starting."
    tornado.ioloop.IOLoop.instance().start()

