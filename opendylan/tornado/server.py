# Copyright (c) 2012, Dylan Hackers.
# See License.txt for details.

import tornado.ioloop
import tornado.web
from opendylan.tornado.handlers import DylanBuildHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/build", DylanBuildHandler)
])

if __name__ == "__main__":
    print "Listening..."
    application.listen(8888)
    print "Starting."
    tornado.ioloop.IOLoop.instance().start()

